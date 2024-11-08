import time
import traceback
import os


from . import utils
from .utils import TrackEvalException
from . import _timing
from .metrics import Count

try:
    import tqdm
    TQDM_IMPORTED = True
except ImportError as _:
    TQDM_IMPORTED = False


class Evaluator:
    """Evaluator class for evaluating different metrics for different datasets"""

    @staticmethod
    def get_default_eval_config():
        """Returns the default config values for evaluation"""
        code_path = utils.get_code_path()
        default_config = {
            'USE_PARALLEL': False,
            'NUM_PARALLEL_CORES': 8,
            'BREAK_ON_ERROR': True,  # Raises exception and exits with error
            'RETURN_ON_ERROR': False,  # if not BREAK_ON_ERROR, then returns from function on error
            'LOG_ON_ERROR': os.path.join(code_path, 'error_log.txt'),  # if not None, save any errors into a log file.

            'PRINT_RESULTS': True,
            'PRINT_ONLY_COMBINED': False,
            'PRINT_CONFIG': False,
            'TIME_PROGRESS': False,
            'DISPLAY_LESS_PROGRESS': True,

            'OUTPUT_SUMMARY': True,
            'OUTPUT_EMPTY_CLASSES': False,  # If False, summary files are not output for classes with no detections
            'OUTPUT_DETAILED': False,
            'PLOT_CURVES': True,
        }
        return default_config

    def __init__(self, config=None):
        """Initialise the evaluator with a config file"""
        self.config = utils.init_config(config, self.get_default_eval_config(), 'Eval')
        # Only run timing analysis if not run in parallel.
        if self.config['TIME_PROGRESS'] and not self.config['USE_PARALLEL']:
            _timing.DO_TIMING = True
            if self.config['DISPLAY_LESS_PROGRESS']:
                _timing.DISPLAY_LESS_PROGRESS = True

    @_timing.time
    def evaluate(self, dataset_list, metrics_list, show_progressbar=False):  # 计算数据集的指标
        """Evaluate a set of metrics on a set of datasets"""
        metric_result =[]  # 结果初始化
        config = self.config  # 读取配置
        metrics_list = metrics_list + [Count()]  # 输出指标+id个数
        metric_names = utils.validate_metrics_list(metrics_list)  # 获取指标名字
        dataset_names = [dataset.get_name() for dataset in dataset_list]  # berrybox 数据名
        output_res = {}  # 输出结果
        output_msg = {}  # 输出信息（是否成功）

        for dataset, dataset_name in zip(dataset_list, dataset_names):
            # 输出信息
            output_res[dataset_name] = {}
            output_msg[dataset_name] = {}
            tracker_list, seq_list, class_list = dataset.get_eval_info()
            print('\nEvaluating %i tracker(s) on %i sequence(s) for %i class(es) on %s dataset using the following '
                  'metrics: %s\n' % (len(tracker_list), len(seq_list), len(class_list), dataset_name,
                                     ', '.join(metric_names)))

            # Evaluate each tracker
            for tracker in tracker_list:  # 一个一个视频追踪
                try:
                    # 进行评估.
                    # returns a nested dict (res), indexed like: res[seq][class][metric_name][sub_metric field]
                    # e.g. res[seq_0001][pedestrian][hota][DetA]
                    print('\nEvaluating %s\n' % tracker)
                    time_start = time.time()
                    res = {}  # 初始化结果
                    if show_progressbar and TQDM_IMPORTED:  # 显示进度条 false
                        seq_list_sorted = sorted(seq_list)
                        for curr_seq in tqdm.tqdm(seq_list_sorted):
                            res[curr_seq] = eval_sequence(curr_seq, dataset, tracker, class_list, metrics_list,
                                                          metric_names)
                    else:
                        for curr_seq in sorted(seq_list):  # 对视频序列进行排序
                            res[curr_seq] = eval_sequence(curr_seq, dataset, tracker, class_list, metrics_list,
                                                          metric_names)  # 对单个视频进行评估

                    # 合并所有序列的结果，然后合并所有类的结果
                    # collecting combined cls keys (cls averaged, det averaged, super classes)

                    combined_cls_keys = []
                    res['COMBINED_SEQ'] = {}
                    # combine sequences for each class
                    for c_cls in class_list:
                        res['COMBINED_SEQ'][c_cls] = {}
                        for metric, metric_name in zip(metrics_list, metric_names):
                            curr_res = {seq_key: seq_value[c_cls][metric_name] for seq_key, seq_value in res.items() if
                                        seq_key != 'COMBINED_SEQ'}
                            res['COMBINED_SEQ'][c_cls][metric_name] = metric.combine_sequences(curr_res)
                    # combine classes
                    if dataset.should_classes_combine:  # 目前为false
                        combined_cls_keys += ['cls_comb_cls_av', 'cls_comb_det_av', 'all']
                        res['COMBINED_SEQ']['cls_comb_cls_av'] = {}
                        res['COMBINED_SEQ']['cls_comb_det_av'] = {}
                        for metric, metric_name in zip(metrics_list, metric_names):
                            cls_res = {cls_key: cls_value[metric_name] for cls_key, cls_value in
                                       res['COMBINED_SEQ'].items() if cls_key not in combined_cls_keys}
                            res['COMBINED_SEQ']['cls_comb_cls_av'][metric_name] = \
                                metric.combine_classes_class_averaged(cls_res)
                            res['COMBINED_SEQ']['cls_comb_det_av'][metric_name] = \
                                metric.combine_classes_det_averaged(cls_res)
                    # combine classes to super classes
                    if dataset.use_super_categories:  # 目前为false
                        for cat, sub_cats in dataset.super_categories.items():
                            combined_cls_keys.append(cat)
                            res['COMBINED_SEQ'][cat] = {}
                            for metric, metric_name in zip(metrics_list, metric_names):
                                cat_res = {cls_key: cls_value[metric_name] for cls_key, cls_value in
                                           res['COMBINED_SEQ'].items() if cls_key in sub_cats}
                                res['COMBINED_SEQ'][cat][metric_name] = metric.combine_classes_det_averaged(cat_res)

                    # 以各种格式打印和输出结果
                    if config['TIME_PROGRESS']:  # 计算时间 false
                        print('\nAll sequences for %s finished in %.2f seconds' % (tracker, time.time() - time_start))
                    output_fol = dataset.get_output_fol(tracker)
                    tracker_display_name = dataset.get_display_name(tracker)
                    metric_result = res  # 计算结果为res
                    for c_cls in res['COMBINED_SEQ'].keys():  # class_list + combined classes if calculated
                        summaries = []
                        details = []
                        num_dets = res['COMBINED_SEQ'][c_cls]['Count']['Dets']
                        if config['OUTPUT_EMPTY_CLASSES'] or num_dets > 0:
                            for metric, metric_name in zip(metrics_list, metric_names):  # 一个一个指标计算
                                # for combined classes there is no per sequence evaluation
                                if c_cls in combined_cls_keys:  # 进不去
                                    table_res = {'COMBINED_SEQ': res['COMBINED_SEQ'][c_cls][metric_name]}
                                else:  # 将对应结果传入table_res
                                    table_res = {seq_key: seq_value[c_cls][metric_name] for seq_key, seq_value
                                                 in res.items()}
                                if config['PRINT_RESULTS'] and config['PRINT_ONLY_COMBINED']:  # 不合并
                                    dont_print = dataset.should_classes_combine and c_cls not in combined_cls_keys
                                    if not dont_print:
                                        metric.print_table({'COMBINED_SEQ': table_res['COMBINED_SEQ']},
                                                           tracker_display_name, c_cls)
                                elif config['PRINT_RESULTS']:  # 打印结果
                                    metric.print_table(table_res, tracker_display_name, c_cls)
                                    # pass
                                if config['OUTPUT_SUMMARY']:
                                    summaries.append(metric.summary_results(table_res))
                                if config['OUTPUT_DETAILED']:
                                    details.append(metric.detailed_results(table_res))
                                if config['PLOT_CURVES']:
                                    metric.plot_single_tracker_results(table_res, tracker_display_name, c_cls,
                                                                       output_fol)
                            if config['OUTPUT_SUMMARY']:
                                utils.write_summary_results(summaries, c_cls, output_fol)
                            if config['OUTPUT_DETAILED']:
                                utils.write_detailed_results(details, c_cls, output_fol)

                    # Output for returning from function
                    output_res[dataset_name][tracker] = res
                    output_msg[dataset_name][tracker] = 'Success'

                except Exception as err:
                    output_res[dataset_name][tracker] = None
                    if type(err) == TrackEvalException:
                        output_msg[dataset_name][tracker] = str(err)
                    else:
                        output_msg[dataset_name][tracker] = 'Unknown error occurred.'
                    print('Tracker %s was unable to be evaluated.' % tracker)
                    print(err)
                    traceback.print_exc()
                    if config['LOG_ON_ERROR'] is not None:
                        with open(config['LOG_ON_ERROR'], 'a') as f:
                            print(dataset_name, file=f)
                            print(tracker, file=f)
                            print(traceback.format_exc(), file=f)
                            print('\n\n\n', file=f)
                    if config['BREAK_ON_ERROR']:
                        raise err
                    elif config['RETURN_ON_ERROR']:
                        return output_res, output_msg

        return output_res, output_msg, metric_result


@_timing.time
def eval_sequence(seq, dataset, tracker, class_list, metrics_list, metric_names):
    """Function for evaluating a single sequence"""
    # 评估单个视频
    raw_data = dataset.get_raw_seq_data(tracker, seq)  # 提取数据集数据
    seq_res = {}
    for cls in class_list:
        seq_res[cls] = {}  # 对每个类别进行评估
        data = dataset.get_preprocessed_seq_data(raw_data, cls)  #
        for metric, met_name in zip(metrics_list, metric_names):
            seq_res[cls][met_name] = metric.eval_sequence(data)
    return seq_res  # 单个视频结果

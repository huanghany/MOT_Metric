import sys
import os
import argparse

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import trackeval  # noqa: E402

if __name__ == '__main__':
    # 获取默认配置:
    default_eval_config = trackeval.Evaluator.get_default_eval_config()  # 评估器配置
    default_dataset_config = trackeval.datasets.BerryBox.get_default_dataset_config()  # 数据集配置
    default_metrics_config = {'METRICS': ['HOTA', 'CLEAR', 'Identity'], 'THRESHOLD': 0.5}  # 指标配置

    default_dataset_config['GT_FOLDER'] = 'data/mydata/gt/'
    default_dataset_config['TRACKERS_FOLDER'] = 'data/mydata/trackers/'
    default_dataset_config['BENCHMARK'] = 'test1'

    config = {**default_eval_config, **default_dataset_config, **default_metrics_config}  # 合并配置
    parser = argparse.ArgumentParser()  # 解析命令行参数
    for setting in config.keys():
        if type(config[setting]) == list or type(config[setting]) == type(None):
            parser.add_argument("--" + setting, nargs='+')
        else:
            parser.add_argument("--" + setting)
    args = parser.parse_args().__dict__
    for setting in args.keys():  # 判断参数类型并转换
        if args[setting] is not None:
            if type(config[setting]) == type(True):  # 布尔类型处理
                if args[setting] == 'True':
                    x = True
                elif args[setting] == 'False':
                    x = False
                else:
                    raise Exception('Command line parameter ' + setting + 'must be True or False')
            elif type(config[setting]) == type(1):  # 整数类型处理
                x = int(args[setting])
            elif type(args[setting]) == type(None):
                x = None
            elif setting == 'SEQ_INFO':  # 特殊处理序列信息
                x = dict(zip(args[setting], [None]*len(args[setting])))
            else:
                x = args[setting]
            config[setting] = x
    eval_config = {k: v for k, v in config.items() if k in default_eval_config.keys()}  # 再分成三部分
    dataset_config = {k: v for k, v in config.items() if k in default_dataset_config.keys()}
    metrics_config = {k: v for k, v in config.items() if k in default_metrics_config.keys()}

    # 进行评估
    evaluator = trackeval.Evaluator(eval_config)
    dataset_list = [trackeval.datasets.BerryBox(dataset_config)]
    metrics_list = []
    for metric in [trackeval.metrics.HOTA, trackeval.metrics.CLEAR, trackeval.metrics.Identity, trackeval.metrics.VACE]:
        if metric.get_name() in metrics_config['METRICS']:
            metrics_list.append(metric(metrics_config))
    if len(metrics_list) == 0:
        raise Exception('No metrics selected for evaluation')

    _, _, analyze_result= evaluator.evaluate(dataset_list, metrics_list)  # 进入评估器评估
    # 输出结果
    tracker_list, seq_list, class_list = dataset_list[0].get_eval_info()
    # print(tracker_list)
    # print(seq_list)
    # print(class_list)
    # print(analyze_result[0])
    for i in seq_list:
        metric_result = analyze_result[i][class_list[0]]
        print(i)
        print("HOTA:", metric_result['HOTA']['HOTA'])
        print("MOTA:", metric_result['CLEAR']['MOTA'])
        print("MOTP:", metric_result['CLEAR']['MOTP'])
        print("IDF1:", metric_result['Identity']['IDF1'])
    # 保存结果

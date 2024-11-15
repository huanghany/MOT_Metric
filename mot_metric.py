import sys
import os
import argparse
import numpy as np
import pandas as pd
from joblib.externals.cloudpickle import instance

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import trackeval  # noqa: E402

if __name__ == '__main__':
    # 获取默认配置:
    default_eval_config = trackeval.Evaluator.get_default_eval_config()  # 评估器配置
    default_dataset_config = trackeval.datasets.BerryBox.get_default_dataset_config()  # 数据集配置
    default_metrics_config = {'METRICS': ['HOTA', 'CLEAR', 'Identity'], 'THRESHOLD': 0.5}  # 指标配置

    default_dataset_config['GT_FOLDER'] = 'data/mydata/gt/'
    default_dataset_config['TRACKERS_FOLDER'] = 'data/mydata/trackers/'
    default_dataset_config['BENCHMARK'] = 'berry-2'
    default_dataset_config['SPLIT_TO_EVAL'] = 'test'

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
                x = dict(zip(args[setting], [None] * len(args[setting])))
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

    _, _, analyze_result = evaluator.evaluate(dataset_list, metrics_list)  # 进入评估器评估
    # 保存结果
    tracker_list, seq_list, class_list = dataset_list[0].get_eval_info()
    # print(tracker_list)
    # print(seq_list)
    # print(class_list)
    # print(analyze_result[0])
    results = {}
    for i in seq_list:
        metric_result = analyze_result[i][class_list[0]]
        results[i] = {
            "GT_id_num": metric_result['Count']['GT_IDs'],
            "T_id_num": metric_result['Count']['IDs'],
            "Total_diff": metric_result['Count']['IDs'] - metric_result['Count']['GT_IDs'],  # 总数差
            "Error_rate": "{0:1.5g}".format(100* (metric_result['Count']['IDs'] - metric_result['Count']['GT_IDs'])
                            / metric_result['Count']['GT_IDs']),  # 总数准确率
            "HOTA": "{0:1.5g}".format(100* np.mean(metric_result['HOTA']['HOTA'])),  # 平均值
            "MOTA": "{0:1.5g}".format(100* metric_result['CLEAR']['MOTA']),
            "MOTP": "{0:1.5g}".format(100*(metric_result['CLEAR']['MOTP'])),
            "IDF1": "{0:1.5g}".format(100* metric_result['Identity']['IDF1'])
        }
        for key, value in metric_result['CLEAR'].items():
            if isinstance(value, float):
                results[i][key] = "{0:1.5g}".format(100 * value)
            else:
                results[i][key] = value
    # 打印结果 
    # print(results)
    for test_name, metrics in results.items():
        print(test_name)
        print("HOTA:", metrics['HOTA'])
        print("MOTA:", metrics['MOTA'])
        print("MOTP:", metrics['MOTP'])
        print("IDF1:", metrics['IDF1'])

    # 保存结果
    results_df = pd.DataFrame.from_dict(results, orient='index')
    results_df.to_csv('evaluation_results_bot_1.csv', index_label='Test Name')
    print("结果已保存至"'evaluation_results_bot_1.csv')


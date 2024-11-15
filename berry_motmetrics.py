import motmetrics as mm
import numpy as np
import pandas as pd
import os
from collections import namedtuple

# 定义 namedtuple 来存储结果
Result = namedtuple('Result', [
    'gt_file', 'track_file', 'gt_unique_ids', 'track_unique_ids',
    'total_difference', 'accuracy', 'mota', 'motp', 'idf1'
])

my_metrics = ['num_frames', 'idf1', 'idp', 'idr',
               'recall', 'precision', 'num_objects',
               'mostly_tracked', 'partially_tracked',
               'mostly_lost', 'num_false_positives',
               'num_misses', 'num_switches',
               'num_fragmentations', 'mota', 'motp']

def motMetricsEnhancedCalculator(gtSource, tSource):
    gt = np.loadtxt(gtSource, delimiter=',', usecols=(0, 2, 3, 4, 5, 6))
    t = np.loadtxt(tSource, delimiter=',', usecols=(0, 2, 3, 4, 5, 6))

    acc = mm.MOTAccumulator(auto_id=True)

    for frame in range(int(gt[:, 0].max())):
        frame += 1
        gt_dets = gt[gt[:, 0] == frame, 1:6]
        t_dets = t[t[:, 0] == frame, 1:6]

        C = mm.distances.iou_matrix(gt_dets[:, 1:], t_dets[:, 1:], max_iou=0.5)
        acc.update(gt_dets[:, 0].astype('int').tolist(),
                   t_dets[:, 0].astype('int').tolist(), C)

    mh = mm.metrics.create()
    summary = mh.compute(acc, metrics=my_metrics, name='acc')

    return summary

def read_file(file_path):
    ids_set = set()
    with open(file_path, 'r') as f:
        for line in f:
            data = line.strip().split(',')
            object_id = data[2]
            ids_set.add(object_id)
    return ids_set

def compare_ids(gt_file, result_file):
    gt_ids = read_file(gt_file)
    result_ids = read_file(result_file)

    gt_unique_ids = len(gt_ids)
    result_unique_ids = len(result_ids)
    total_difference = result_unique_ids - gt_unique_ids

    accuracy = 1 - (total_difference / gt_unique_ids) if gt_unique_ids > 0 else 0

    return gt_unique_ids, result_unique_ids, total_difference, accuracy

def save_to_csv(results, output_file):
    df = pd.DataFrame([result._asdict() for result in results])
    df.to_csv(output_file, index=False)

def process_directory(directory_path, output_directory):
    results = []  # 在函数内部定义结果列表
    gt_files = []
    track_files = []

    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith("gt.txt"):
                gt_files.append(os.path.join(root, file))
            elif file.endswith("track_results.txt"):
                track_files.append(os.path.join(root, file))

    for gt_file in gt_files:
        file_prefix = os.path.basename(gt_file).replace("gt.txt", "track_results.txt")
        matching_track_file = next((track for track in track_files if file_prefix in os.path.basename(track)), None)

        if matching_track_file:
            result = get_results(gt_file, matching_track_file)
            print(result)
            results.append(result)

    return results

def get_results(gt_file, matching_track_file):
    gt_unique_ids, result_unique_ids, total_diff, accuracy = compare_ids(gt_file, matching_track_file)
    mot_summary = motMetricsEnhancedCalculator(gt_file, matching_track_file)
    df = pd.DataFrame(mot_summary)
    result = Result(
        gt_file=os.path.basename(gt_file),
        track_file=os.path.basename(matching_track_file),
        gt_unique_ids=gt_unique_ids,
        track_unique_ids=result_unique_ids,
        total_difference=total_diff,
        accuracy=accuracy,
        mota=df['mota'].values[0],
        motp=df['motp'].values[0],
        idf1=df['idf1'].values[0]
    )
    return result


if __name__ == "__main__":
    directory_path = r"D:\华毅\目标追踪数据集"
    output_directory = directory_path
    output_file = os.path.join(output_directory, 'combined_results.csv')

    results = process_directory(directory_path, output_directory)

    # 保存所有结果到同一个CSV文件
    save_to_csv(results, output_file)
    print(f"所有结果已保存到 {output_file}")

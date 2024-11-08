import os
import csv


# 读取文件并统计唯一ID数量
def read_file(file_path):
    ids_set = set()  # 用set来存储ID，避免重复
    with open(file_path, 'r') as f:
        for line in f:
            data = line.strip().split(',')  # 假设数据是逗号分隔
            object_id = data[2]  # 只关心第三列的ID
            ids_set.add(object_id)  # 添加ID到集合中
    return ids_set  # 返回唯一ID的集合


# 比较两个文件中唯一ID数量的差异
def compare_ids(gt_file, result_file):
    gt_ids = read_file(gt_file)  # 获取gt文件的唯一ID集合
    result_ids = read_file(result_file)  # 获取result文件的唯一ID集合

    # 计算唯一ID的数量
    gt_unique_ids = len(gt_ids)
    result_unique_ids = len(result_ids)
    # 计算唯一ID的总数差异
    total_difference = result_unique_ids - gt_unique_ids

    # 计算准确率
    accuracy = 1 - (total_difference / gt_unique_ids) if gt_unique_ids > 0 else 0

    return gt_unique_ids, result_unique_ids, total_difference, accuracy  # 返回唯一ID总数、差异和准确率


# 保存结果到CSV文件
def save_to_csv(gt_unique_ids, result_unique_ids, total_diff, accuracy, output_file):
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # 写入总数行
        writer.writerow(['GT文件ID数', 'track文件ID数', '数量差异', '准确率'])
        writer.writerow([gt_unique_ids, result_unique_ids, total_diff, accuracy])


# 查找目录中的文件并进行比较
def process_directory(directory_path, output_directory):
    gt_files = []  # 存放所有的gt文件
    track_files = []  # 存放所有的track文件

    # 遍历目录查找符合条件的文件
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith("gt.txt"):  # 查找gt文件
                gt_files.append(os.path.join(root, file))
            elif file.endswith("track_results.txt"):  # 查找track文件
                track_files.append(os.path.join(root, file))

    # 确保每个gt文件都有对应的track文件
    for gt_file in gt_files:
        file_prefix = os.path.basename(gt_file).replace("gt.txt", "track_results.txt")
        # 在track文件中找到与gt文件对应的文件
        matching_track_file = next((track for track in track_files if file_prefix in os.path.basename(track)), None)

        if matching_track_file:
            # 比较并保存结果
            gt_unique_ids, result_unique_ids, total_diff, accuracy = compare_ids(gt_file, matching_track_file)
            file_prefix = os.path.basename(gt_file).replace("gt.txt", "")
            output_file = os.path.join(output_directory, f"{file_prefix}result.csv")

            # 输出结果
            print(f"处理文件: {gt_file} 和 {matching_track_file}")
            print(f"GT文件ID总数: {gt_unique_ids}")
            print(f"track文件ID总数: {result_unique_ids}")
            print(f"总数差异: {total_diff}")
            print(f"准确率: {accuracy:.2%}")

            # 保存到CSV文件
            save_to_csv(gt_unique_ids, result_unique_ids, total_diff, accuracy, output_file)
            print(f"结果已保存到 {output_file}")


if __name__ == "__main__":
    # 指定输入和输出目录
    # directory_path = 'data/test_2'  # 文件所在的目录
    directory_path = r"D:\华毅\目标追踪数据集\1_艾维"  # 文件所在的目录

    output_directory = directory_path  # 保存结果的目录
    # output_directory = 'data/test_2'
    # 确保输出目录存在
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # 处理目录下的文件
    process_directory(directory_path, output_directory)

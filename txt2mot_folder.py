import os


def change_t(input_file, output_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()

    with open(output_file, 'w') as file:  # 保存到新的文件
        for line in lines:
            parts = line.strip().split(',')
            if parts[1] == 'Flower_':  # 检查第二列内容
                continue  # 如果是'flower_'，则跳过该行
            # 第一列加一
            parts[0] = str(int(parts[0]) + 1)
            parts.pop(1)  # 去掉第二列
            parts[6:10] = ['1', '-1', '-1', '-1']  # 修改第8-10位为1
            file.write(','.join(parts) + '\n')


def process_folder(folder_path, output_folder):
    # 确保输出文件夹存在
    os.makedirs(output_folder, exist_ok=True)

    # 遍历文件夹中的所有文件
    for filename in os.listdir(folder_path):
        # 仅处理文件名中包含 "_track_results_" 的 .txt 文件
        if '_track_results_' in filename and filename.endswith('.txt'):
            input_file = os.path.join(folder_path, filename)
            output_file = os.path.join(output_folder, filename)  # 输出文件路径与输入文件名一致
            change_t(input_file, output_file)
            print(f"处理完成: {filename}")


# 示例文件夹路径
input_folder = r'D:\华毅\目标追踪数据集\result'
output_folder = r'D:\华毅\目标追踪\MOT_Metric\data\mydata\trackers\berry-2-test\berry-3'

# 执行批量处理
process_folder(input_folder, output_folder)

def change_gt(input_file, output_file):
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
            parts[6:9] = ['1', '1', '1']  # 修改第8-10位为1
            parts.pop(9)  # 去掉第10列
            file.write(','.join(parts) + '\n')


def change_t(input_file_1, output_file_1):
    with open(input_file_1, 'r') as file:
        lines = file.readlines()

    with open(output_file_1, 'w') as file:  # 保存到新的文件
        for line in lines:
            parts = line.strip().split(',')
            if parts[1] == 'Flower_':  # 检查第二列内容
                continue  # 如果是'flower_'，则跳过该行
            # 第一列加一
            parts[0] = str(int(parts[0]) + 1)
            parts.pop(1)  # 去掉第二列
            parts[6:10] = ['1', '-1', '-1', '-1']  # 修改第8-10位为1
            # parts.pop(9)  # 去掉第10列
            file.write(','.join(parts) + '\n')


def modify_gt(input_file, output_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()

    with open(output_file, 'w') as file:  # 保存到新的文件
        for line in lines:
            parts = line.strip().split(',')
            if parts[1] == 'Flower_':  # 检查第二列内容
                continue  # 如果是'flower_'，则跳过该行
            # 第一列加一
            parts[0] = str(int(parts[0]))
            # parts.pop(1)  # 去掉第二列
            # parts[6:9] = ['1', '1', '1']  # 修改第8-10位为1
            parts[7:11] = ['-1', '-1', '-1', '0']  # 修改第8-10位为1
            # parts.pop(9)  # 去掉第10列
            file.write(','.join(parts) + '\n')


# 示例文件路径
# input_file = r'D:\华毅\目标追踪数据集\train\L1_2_gt.txt'
input_file_1 = r'D:\华毅\目标追踪数据集\1_艾维\20240113-103852_rack-1_left_RGB_track_results_strong_berry_1.txt'

# output_file = r'D:\华毅\目标追踪\MOT_Metric\data\mydata\gt\berry-1-train\L1_osnet\gt.txt'
# output_file = r'D:\华毅\目标追踪数据集\train\L3_2_gt.txt'
output_file_1 = r'D:\华毅\目标追踪\MOT_Metric\data\mydata\trackers\berry-1-test\berry-3\aiwei_1_strongsort_berry_1.txt'

# change_gt(input_file, output_file)
# modify_gt(input_file, output_file)
change_t(input_file_1, output_file_1)

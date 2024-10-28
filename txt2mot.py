# input_file = r'D:\华毅\boxmot\data\test_3\result/part1_track_results_1.txt'
input_file = r'D:\华毅\目标追踪数据集\1_艾维\20240113-103852_rack-1_left_RGB_track_results.txt'
output_file = r'D:\华毅\目标追踪\TrackEval\data\gt\mydata\test1-train\test-3\test-3.txt'

with open(input_file, 'r') as file:
    lines = file.readlines()

with open(output_file, 'w') as file:  # 保存到新的文件
    for line in lines:
        parts = line.strip().split(',')
        # gt
        # parts[6:9] = ['1', '1', '1']  # 修改7-9位为1
        # parts.pop(9)  # 去掉第十位
        # track
        parts[6:10] = ['1', '-1', '-1', '-1']  # 修改7-10位

        file.write(','.join(parts) + '\n')

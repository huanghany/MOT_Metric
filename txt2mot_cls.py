input_file = r'D:\华毅\目标追踪数据集\1_艾维\20240113-103852_rack-1_left_RGB_gt.txt'
output_file = r'D:\华毅\目标追踪\TrackEval\data\gt\mydata\test1-train\test-3\gt\gt.txt'

# 定义字符与数字的对应关系
mapping = {
    'Ripe_': 1,
    'Ripe7_': 2,
    'Ripe4_': 3,
    'Ripe2_': 4,
    'Unripe_': 5,
    'Flower_': 6,
    'Disease_': 7
}

with open(input_file, 'r') as file:
    lines = file.readlines()

with open(output_file, 'w') as file:  # 保存到新的文件
    for line in lines:
        parts = line.strip().split(',')

        # 转换第二列的字符为数字
        if parts[1] in mapping:
            parts[1] = str(mapping[parts[1]])

        parts[7:10] = ['1', '1', '1']  # 修改7-9位为1
        parts.pop(10)  # 去掉第十位
        file.write(','.join(parts) + '\n')

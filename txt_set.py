def remove_duplicate_lines(input_file, output_file):
    # 用集合来存储唯一的行
    unique_lines = set()

    with open(input_file, 'r') as file:
        lines = file.readlines()

    # 去除重复行
    for line in lines:
        unique_lines.add(line)

    # 写入去重后的内容到新的文件
    with open(output_file, 'w') as file:
        for line in unique_lines:
            file.write(line)


# 使用示例
input_file = r'D:\华毅\目标追踪数据集\1_艾维\20240113-104949_rack-5_right_RGB_gt.txt'
output_file = r'D:\华毅\目标追踪数据集\1_艾维\1.txt'
remove_duplicate_lines(input_file, output_file)

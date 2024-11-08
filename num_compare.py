
import csv
import glob
import os

# 指定文件夹路径
folder_path = r'D:\华毅\目标追踪数据集\train'  # 替换为实际的文件夹路径

# 查找文件夹中所有包含 'result' 的 .txt 文件
files = glob.glob(os.path.join(folder_path, '*result*.txt'))

# 定义行标题
categories = ["Unripe", "Ripe", "Ripe7", "Ripe4", "Ripe2", "Flower", "Disease"]


# 读取单个文件的内容
def read_data(file):
    data = {}
    with open(file, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            if ':' in line:
                key, value = line.strip().split(':')
                data[key.strip()] = value.strip()
    return data


# 读取所有文件的数据
all_data = []
for file in files:
    file_data = read_data(file)
    all_data.append(file_data)

# 将数据写入CSV文件
with open('output.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    # 写入表头，文件名作为列标题
    writer.writerow(['Category'] + [os.path.basename(file) for file in files])

    # 按照指定的行标题顺序写入数据
    for category in categories:
        row = [category]
        for data in all_data:
            row.append(data.get(category, '0'))  # 如果数据不存在，则填充'0'
        writer.writerow(row)

print("数据已成功写入 output.csv")

# MOT_Metric

## **📌 项目简介**

MOT_Metric 是一个用于评估目标跟踪效果的工具，可计算多种目标跟踪评价指标，包括 **HOTA**、**MOTA**、**MOTP**、**IDF1** 等。  
此工具基于 [TrackEval](https://github.com/JonathonLuiten/TrackEval/) 进行开发和改进。

---

## **📁 仓库结构**

```plaintext
├── data                数据存放目录
│   ├── mydata          子数据集目录
│       ├── gt          真值存放目录
│       ├── trackers    追踪结果存放目录
│   ├── results         结果存放目录
├── trackeval           评估库
├── mot_metric.py       评估主程序
├── txt2mot.py          数据格式化脚本（修改文件列尾为 1, 1, 1）
├── txt2mot_cls.py      数据格式化脚本（将类别转换为对应数字）
```

---

## **🔧 使用说明**

### **安装依赖**

该工具适用于 Python 3.7 - 3.11 环境。  

- 安装所有依赖：  
  ```bash
  pip3 install -r requirements.txt
  ```

- 如果只需最小依赖（无额外功能）：  
  ```bash
  pip3 install -r minimum_requirements.txt
  ```

---

### **运行示例**

#### 数据组织

将真值（`gt`）和追踪结果（`trackers`）放在 `data/mydata/` 文件夹下。以下是一个示例结构：  

假设有两个视频：`video1` 和 `video2`，并且这两个视频已经进行了多目标跟踪。则文件组织方式如下：  

```plaintext
├── gt
│   ├── test1-train
│       ├── video1
│           ├── gt.txt       # 真值文件
│           ├── seqinfo.ini  # video1视频具体信息
│       ├── video2
│           ├── gt.txt       # 真值文件
│           ├── seqinfo.ini  # video2视频具体信息
├── trackers
│   ├── test1-train
│       ├── video1.txt       # video1追踪结果文件
│       ├── video2.txt       # video2追踪结果文件
```

**文件格式要求**  

真值文件与追踪结果文件的格式相同，具体如下：  

```plaintext
帧号, ID, x, y, w, h, 1, 1, 1
10,  1, 660, 2116, 28, 63, 1, 1, 1
10,  2, 101, 3247, 37, 61, 1, 1, 1
10,  3,  68,  517, 23, 40, 1, 1, 1
...
```

每一行的内容说明：  
- **帧号**：目标所在帧的编号。  
- **ID**：目标的唯一标识符。  
- **x, y, w, h**：目标的边界框的左上角x,y坐标及边界框的宽和高。  
- **最后三位固定为 1**。

---

#### seqinfo.ini 文件  

`seqinfo.ini` 文件用于记录视频相关的基本信息。其格式如下：  

```plaintext
[Sequence]
name=aiwei_1_botsort_3      # 视频名称
imDir=img1                  # 图像文件夹路径
frameRate=30                # 视频帧率（fps）
seqLength=2360              # 视频帧数
imWidth=1280                # 图像宽度
imHeight=720                # 图像高度
imExt=.jpg                  # 图像文件扩展名
```

字段说明：  
- **name**：视频的名称，可自定义。  
- **imDir**：存放图像帧的文件夹名称。  
- **frameRate**：视频的帧率，用于评估时的时间单位换算。  
- **seqLength**：视频帧的总数量。  
- **imWidth** 和 **imHeight**：每一帧图像的分辨率（宽度和高度）。  
- **imExt**：图像文件的后缀名，例如 `.jpg` 或 `.png`。

确保文件内容与实际视频数据对应，否则评估可能失败。

---
### **运行方式**

1. 默认运行：  
   ```bash
   python mot_metric.py
   ```
   将对 `test1` 数据集进行评估。

2. 使用命令行参数运行：  
   ```bash
   python mot_metric.py --BENCHMARK test1 \
                        --CLASSES_TO_EVAL ripe \
                        --METRICS HOTA CLEAR Identity \
                        --NUM_PARALLEL_CORES 1
   ```

---

## **⚙ 参数说明**

| 参数                | 描述                                                                                  | 示例                     |
|---------------------|---------------------------------------------------------------------------------------|--------------------------|
| `--GT_FOLDER`       | 真值文件路径                                                                          | `data/mydata/gt/`        |
| `--OUTPUT_FOLDER`   | 结果保存路径                                                                          | `data/results/`          |
| `--CLASSES_TO_EVAL` | 要评估的类别（小写字母或数字）                                                        | `ripe`                   |
| `--BENCHMARK`       | 数据集名称                                                                            | `test1-train`            |
| `--DO_PREPROC`      | 是否执行预处理（布尔值）                                                              | `False`                  |
| `--METRICS`         | 选择的评估指标：HOTA, CLEAR, Identity（多个指标用空格分隔）                           | `HOTA CLEAR`             |
| `--NUM_PARALLEL_CORES` | 并行核数量                                                                         | `1`                      |

---

## **📊 输出说明**

运行后输出结果为字典格式，包含各指标的详细结果，例如：  

```plaintext
test-1:
HOTA: 0.98422
MOTA: 0.9803113553113553
MOTP: 0.9998710003685704
IDF1: 0.9878412479926588

test-2:
HOTA: 0.95435
...
```

如果需要更直观的结果，可以生成 CSV 文件（如 [evaluation_results.csv](result/example/evaluation_results.csv)）查看。

---

## **📄 许可证**

MOT_Metric 遵循 [MIT 许可证](LICENSE)。  

**评估指标的具体计算来源**：  
[https://github.com/JonathonLuiten/TrackEval](https://github.com/JonathonLuiten/TrackEval/)

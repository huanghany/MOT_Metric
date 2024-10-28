
# MOT_Metric
*用于评估目标跟踪的代码.*

*此代码库基于[TrackEval](https://github.com/JonathonLuiten/TrackEval/)官方库的基础进行更改*

此代码库用于计算目标追踪评价指标，包含HOTA,MOTA,MOTP，IDF1等

## 仓库结构

```text
├── data 数据集存放位置
│   ├── mydata 子数据集目录
│       ├── gt 真值存放位置
│       ├── trackers 追踪结果存放位置
│   ├── results 结果存放位置
├── trackeval 评估库 
├── mot_metric.py 评估API
├── txt2mot.py 数据集格式化脚本（修改后三位）
├── txt2mot_cls.py  数据集格式化脚本（将类别转换为对应数字）
```

## 数据

你可以将你的数据，真实（gt）和测试（test）文件放在`data/mydata/`文件夹下，这是一个例子：

你现在有两个视频，video1和video2，这两个视频你都进行了多目标跟踪。那么你需要这样组织你的文件夹：
```
gt/
    test1-train/
            seq-01/   # 视频名
                gt.txt          # <---- ground truth
            seqinfo.ini         # 放你的视频的信息
trackers/   # 你自己代码运行出来的结果
    test1-train/
            berry/
                seq-01.txt          # <---- model result 视频名.txt
```

**至于每个文件中的格式，直接参照我的就行，比如：**
```
10,1,660,2116,28,63,1,1,1
10,2,101,3247,37,61,1,1,1
10,3,68,517,23,40,1,1,1
...
```
**每行的第一个数是帧号；第二个数是id；后面接着的四个数表示框的位置和大小；最后三个数固定**

## Running the code

直接运行(进行test1数据集评估)
```
python mot_metric.py 
```

或者带命令行参数
```
python mot_metric.py --BENCHMARK test1  --CLASSES_TO_EVAL ripe --METRICS HOTA CLEAR Identity  --NUM_PARALLEL_CORES 1
```

## 参数说明

```
--GT_FOLDER # gt路径
--OUTPUT_FOLDER # 结果保存路径
--CLASSES_TO_EVAL  # 要评估的类别 为小写字母和数字,如：unripe
--BENCHMARK ai_city   # 视频名
--DO_PREPROC False 
--METRICS HOTA # 选择测评指标 'HOTA', 'CLEAR', 'Identity'
```

## 输出说明

当前输出为一个result字典
```
test-1:
HOTA: 0.98422
MOTA: 0.9803113553113553
MOTP: 0.9998710003685704
IDF1: 0.9878412479926588
test-2:
...
```

## Requirements
 Code tested on Python 3.7.
 
 - Minimum requirements: numpy, scipy
 - For plotting: matplotlib
 - For segmentation datasets (KITTI MOTS, MOTS-Challenge, DAVIS, YouTube-VIS): pycocotools
 - For DAVIS dataset: Pillow
 - For J & F metric: opencv_python, scikit_image
 - For simples test-cases for metrics: pytest

use ```pip3 -r install requirements.txt``` to install all possible requirements.

use ```pip3 -r install minimum_requirments.txt``` to only install the minimum if you don't need the extra functionality as listed above.

## License

MOT_Metric is released under the [MIT License](LICENSE).


## Citing TrackEval

If you use this code in your research, please use the following BibTeX entry:

```BibTeX
@misc{luiten2020trackeval,
  author =       {Jonathon Luiten, Arne Hoffhues},
  title =        {TrackEval},
  howpublished = {\url{https://github.com/JonathonLuiten/TrackEval}},
  year =         {2020}
}
```

Furthermore, if you use the HOTA metrics, please cite the following paper:

```
@article{luiten2020IJCV,
  title={HOTA: A Higher Order Metric for Evaluating Multi-Object Tracking},
  author={Luiten, Jonathon and Osep, Aljosa and Dendorfer, Patrick and Torr, Philip and Geiger, Andreas and Leal-Taix{\'e}, Laura and Leibe, Bastian},
  journal={International Journal of Computer Vision},
  pages={1--31},
  year={2020},
  publisher={Springer}
}
```
citing
If you use any other metrics please also cite the relevant papers, and don't forget to cite each of the benchmarks you evaluate on.


# MOT_Metric
*用于评估目标跟踪的代码.*

*此代码库基于[TrackEval](https://github.com/JonathonLuiten/TrackEval/)官方库的基础进行更改*

此代码库用于计算目标追踪评价指标，包含HOTA,MOTA,MOTP，IDF1等

## 仓库结构

```text
├── data 数据集存放位置
│   ├── gt 真值存放位置
│   ├── trackers 追踪结果存放位置
├── trackeval 评估库 
├── txt2metric.py 评估API
├── txt2mot.py 数据集格式化脚本（修改后三位）
├── txt2mot_cls.py  数据集格式化脚本（将类别转换为对应数字）
```

## 数据

你可以将你的数据，真实（gt）和测试（test）文件放在`data/`文件夹下，这是一个例子：

你现在有两个视频，video1和video2，这两个视频你都进行了多目标跟踪。那么你需要这样组织你的文件夹：
```
--video1/gt/gt.txt          # video1的gt文件
--video2/gt/gt.txt          # video2的gt文件
--video1.txt                # video1的test文件
--video2.txt                # video2的test文件
```

**至于每个文件中的格式，直接参照我的就行，比如：**
```
10,1,660,2116,28,63,1,1,1
10,2,101,3247,37,61,1,1,1
10,3,68,517,23,40,1,1,1
...
```
**每行的第一个数是帧号；第二个数是id；后面接着的四个数表示框的位置和大小；最后三个数固定**

## 参数说明

- 输入的评估类别只能为小写字符及数字,
```
['ripe', 'ripe7', 'ripe4', 'ripe2', 'unripe', 'flower', 'disease']
```


## Running the code



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

TrackEval is released under the [MIT License](LICENSE).


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

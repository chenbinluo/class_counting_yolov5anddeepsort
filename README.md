# class_counting_yolov5anddeepsort
## 简介
- 本项目实现对视频文件中的车辆、自行车、行人、狗和其他机动车的识别和计数功能；
- 并且以3秒钟为单位输出每个时间区间内撞击视频检测线的各个类型目标的数量；
- 项目参考repo包括但不限于：
- [yolo v5](https://github.com/ultralytics/yolov5)
- [yolo with deepsort](https://github.com/mikel-brostrom/Yolov5_DeepSort_Pytorch)
- [class counting by dyh](https://github.com/dyh/unbox_yolov5_deepsort_counting)

（本人由衷的感谢上述各位大佬公开的repo！！！）

## 运行环境
- python 3.6+，pip 20+
- pytorch
- cuda
- cudnn
- opencv

## 环境搭建
- [参见此博客](https://blog.csdn.net/qq_45389690/article/details/111306902?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522163722085216780255277225%2522%252C%2522scm%2522%253A%252220140713.130102334.pc%255Fblog.%2522%257D&request_id=163722085216780255277225&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~blog~first_rank_v2~rank_v29-5-111306902.pc_v2_rank_blog_default&utm_term=yolov5%E7%8E%AF%E5%A2%83%E6%90%AD%E5%BB%BA&spm=1018.2226.3001.4450)

## 运行步骤
1.下载代码
- git clone

```
$ git clonehttps://github.com/chenbinluo/class_counting_yolov5anddeepsort.git
```
(建议直接下载zip文件更快些)

2.激活环境

```
activate torch107
```

3. 安装软件包

```
pip install -r requirements.txt
```

4. 运行程序

```
python class_counting.py
```

## 代码输出
- class_counting.py文件下148-157是测试代码是播放检测过程，如需要可以注释掉；
![Image text](https://github.com/chenbinluo/img/blob/main/result.png)
- 最终结果以csv文件保存，class_counting.py会在代码当前路径下新建一个result文件夹，并将结果写入该文件夹的video_counting_result.csv里面，实现这一部分的代码是class_counting.py的61-68行和159-162行；

## 按需更改
- 定义视频撞击横线在class_counting.py文件下的15行更改；
- 更换测试视频在class_counting.py文件下的46行更改；
- 改变检测类别（增加或减少）在class_counting.py文件下52行更改；
- 更改统计时间区间在class_counting.py文件下58行更改；

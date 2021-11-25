import numpy as np
import tracker
from detector import Detector
import cv2
import csv
import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

if __name__ == '__main__':
    # 根据视频尺寸，填充一个polygon，供撞线计算使用
    mask_image_temp = np.zeros((1080, 1920), dtype=np.uint8)

    # 初始化撞线polygon
    list_pts_blue = [[100, 500], [100, 600], [1900, 600], [1900, 500]]
    ndarray_pts_blue = np.array(list_pts_blue, np.int32)
    polygon_blue_value_1 = cv2.fillPoly(mask_image_temp, [ndarray_pts_blue], color=1)
    polygon_blue_value_1 = polygon_blue_value_1[:, :, np.newaxis]

    # 撞线检测用mask，包含1个polygon，供撞线计算使用
    polygon_mask_blue = polygon_blue_value_1  # + polygon_yellow_value_2

    # 缩小尺寸，1920x1080->960x540
    polygon_mask_blue = cv2.resize(polygon_mask_blue, (960, 540))

    # 蓝 色盘 b,g,r
    blue_color_plate = [255, 0, 0]
    # 蓝 polygon图片
    blue_image = np.array(polygon_blue_value_1 * blue_color_plate, np.uint8)

    # 彩色图片（值范围 0-255）
    color_polygons_image = blue_image
    # 缩小尺寸，1920x1080->960x540
    color_polygons_image = cv2.resize(color_polygons_image, (960, 540))

    # list 与蓝色polygon重叠
    list_overlapping_blue_polygon = []

    font_draw_number = cv2.FONT_HERSHEY_SIMPLEX
    draw_text_postion = (int(960 * 0.01), int(540 * 0.05))

    # 初始化 yolov5
    detector = Detector()

    # 打开视频
    capture = cv2.VideoCapture('./video/FLIR_to_video.mp4')

    # 获取视频的帧速率，即每秒视频包含的图片帧数
    fps = capture.get(5)

    # 定义需要追踪的类别
    detector_list = ['person', 'bicycle', 'car', 'dog', 'other_vehicle']

    # 初始化各类别的初始统计数量为0
    output_count = count_dict = dict(zip(detector_list, [0 for _ in range(len(detector_list))]))

    # 初始化输出的时间间隔和初始帧数记录,此处以3秒为单位输出
    t_interval = 3
    frame = 0

    videoWriter = None

    # 建立路径和空的csv，按照57行定义的时间间隔为统计频率，将各个类别撞线统计结果逐步写入csv里面
    result_path = os.path.join(os.getcwd(), 'result')
    isExists = os.path.exists(result_path)
    if not isExists:
        os.makedirs(result_path)
    with open(os.path.join(result_path, 'video_count_result.csv'), 'w+', newline='') as df:
        writer = csv.writer(df)
        writer.writerow(detector_list)

        # 开始按帧检测和追踪视频里面的目标
        while True:
            # 读取每帧图片
            ret, im = capture.read()
            # frame的作用是结合fps来作为计时的函数
            # 基本原理是见line 171
            frame += 1
            if im is None:
                break

            # 缩小尺寸，1920x1080->960x540
            im = cv2.resize(im, (960, 540))

            list_bboxs = []
            bboxes = detector.detect(im, detector_list)

            # 如果画面中有bbox
            if len(bboxes) > 0:
                list_bboxs = tracker.update(bboxes, im)
                # 画框
                # 撞线检测点，(x1，y1)，y方向偏移比例 0.0~1.0
                output_image_frame = tracker.draw_bboxes(im, list_bboxs, line_thickness=None)
                pass
            else:
                # 如果画面中 没有bbox
                output_image_frame = im
            pass

            # 输出图片
            output_image_frame = cv2.add(output_image_frame, color_polygons_image)

            # 开始计数
            if len(list_bboxs) > 0:
                # ----------------------判断撞线----------------------
                for item_bbox in list_bboxs:
                    x1, y1, x2, y2, label, track_id = item_bbox

                    # 撞线检测点，(x1，y1)，y方向偏移比例 0.0~1.0
                    y1_offset = int(y1 + ((y2 - y1) * 0.6))

                    # 撞线的点
                    y = y1_offset
                    x = x1
                    if polygon_mask_blue[y, x] == 1:
                        # 如果撞 蓝polygon
                        if track_id not in list_overlapping_blue_polygon:
                            list_overlapping_blue_polygon.append(track_id)
                            if len(label) > 0:
                                count_dict[label] += 1
                                output_count[label] += 1
                            pass
                        pass
                    else:
                        pass
                    pass
                pass
                # ----------------------清除无用id----------------------
                for id1 in list_overlapping_blue_polygon:
                    is_found = False
                    for _, _, _, _, _, bbox_id in list_bboxs:
                        if bbox_id == id1:
                            is_found = True
                            break
                        pass
                    pass

                    if not is_found:
                        # 如果没找到，删除id
                        if id1 in list_overlapping_blue_polygon:
                            list_overlapping_blue_polygon.remove(id1)
                        pass
                    pass
                pass
                # 清空list
                list_bboxs.clear()
                pass
            else:
                # 如果图像中没有任何的bbox，则清空list
                list_overlapping_blue_polygon.clear()
                pass
            pass

            # 视频画面播放
            text_draw = ''
            for i in detector_list:
                text_draw += i + ' : ' + str(output_count[i]) + ';  '
            output_image_frame = cv2.putText(img=output_image_frame, text=text_draw,
                                             org=draw_text_postion,
                                             fontFace=font_draw_number,
                                             fontScale=1, color=(255, 255, 255), thickness=2)
            cv2.imshow('Visualization', output_image_frame)
            cv2.waitKey(1)

            # 将追踪的结果写入结果文件夹下的result文件里面
            if videoWriter is None:
                fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
                videoWriter = cv2.VideoWriter(os.path.join(result_path, 'detection_result.mp4'), fourcc, fps, (output_image_frame.shape[1], output_image_frame.shape[0]))
            videoWriter.write(output_image_frame)
            pass

            # 计数结果写入csv文件,并把前面一段时间的统计结果清零
            if ret == True and (frame/fps) % t_interval == 0:
                writer.writerow(count_dict.values())
                # 将当前时间区间内的结果写入csv文件之后将类别计数结果清空，开始统计下一个时间区间的结果
                count_dict = dict(zip(detector_list, [0 for _ in range(len(detector_list))]))
            pass
        pass
        capture.release()
        cv2.destroyAllWindows()

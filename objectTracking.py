# -*- coding: utf-8 -*-

# 操作流程：视频播放过程中按“P”暂停播放，随即进行目标的画框圈定
# 鼠标从画框左上角点A托拽到右下角点B，接着输入任意键可显示画框结果，鼠标点击点B，再按“P”实现目标跟踪
# 或者鼠标分别点击画框左上角点A和右下角点B，再按“P”实现目标跟踪，但这样不会显示画框结果

import os
import dlib
import cv2
import numpy as np


# 鼠标事件，返回鼠标托拽的起点和终点坐标
def get_rect(im, title='get_rect'):   # (a,b) = get_rect(im, title='get_rect')
    mouse_params = {'tl': None, 'br': None, 'current_pos': None, 'released_once': False}
    cv2.namedWindow(title)
    cv2.moveWindow(title, 100, 100)

    def onMouse(event, x, y, flags, param):

        param['current_pos'] = (x, y)

        if param['tl'] is not None and not (flags & cv2.EVENT_FLAG_LBUTTON):
            param['released_once'] = True

        if flags & cv2.EVENT_FLAG_LBUTTON:
            if param['tl'] is None:
                param['tl'] = param['current_pos']
            elif param['released_once']:
                param['br'] = param['current_pos']

    cv2.setMouseCallback(title, onMouse, mouse_params)
    cv2.imshow(title, im)

    while mouse_params['br'] is None:
        im_draw = np.copy(im)
        if mouse_params['tl'] is not None:
            cv2.rectangle(im_draw, mouse_params['tl'], mouse_params['current_pos'], (255, 0, 0))
        cv2.imshow(title, im_draw)
        cv2.waitKey(0)

    cv2.destroyWindow(title)

    tl = (min(mouse_params['tl'][0], mouse_params['br'][0]), min(mouse_params['tl'][1], mouse_params['br'][1]))
    br = (max(mouse_params['tl'][0], mouse_params['br'][0]), max(mouse_params['tl'][1], mouse_params['br'][1]))

    # 返回矩形框坐标
    return tl, br

# Path to the video frames
video_folder = os.path.join("examples", "video")

tracker = dlib.correlation_tracker()

tracker_started = False  # 是否已经画框开始追踪

cap = cv2.VideoCapture(0)  # 读取摄像头
if not cap.isOpened():  # 如果未发现摄像头，则按照路径读取视频文件
    cap = cv2.VideoCapture(os.path.join(video_folder, "test.mp4"))  # 读取视频

c = 1

# 用于保存跟踪的视频
fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
fps = 30
size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
out = cv2.VideoWriter('result.mp4', fourcc, fps, size)

while True:
    ret, frame = cap.read()
    if ret:
        print("Processing Frame {}".format(c), ret)
        RGB_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        key = cv2.waitKey(40) & 0xFF
        # 按q结束
        if key == ord("q"):
            break
        # 按p暂停进行画框
        if key == ord("p"):
            cv2.destroyWindow('frame')  # 先关掉，因为下面画框又会显示该帧
            (a, b) = get_rect(frame, title='get_rect')  # 获取鼠标画矩形框坐标
            # print("--------------",a,b)
            tracker.start_track(RGB_img, dlib.rectangle(a[0], a[1], b[0], b[1]))  # 开始追踪
            tracker_started = True
        if tracker_started:
            tracker.update(RGB_img)
            p = tracker.get_position()
            # print(int(p.tl_corner().x), int(p.tl_corner().y), int(p.br_corner().x), int(p.br_corner().y))
            cv2.rectangle(frame, (int(p.tl_corner().x), int(p.tl_corner().y)),
                          (int(p.br_corner().x), int(p.br_corner().y)), (0, 255, 0), 1)  # 画框

        cv2.imshow('frame', frame)  # 重新显示

        # 保存跟踪的视频
        if tracker_started:
            out.write(frame)

        c += 1
    else:
        break

cap.release()
out.release()
cv2.destroyAllWindows()

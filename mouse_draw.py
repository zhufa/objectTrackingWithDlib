# -*- coding: utf-8 -*-

# 鼠标画框实现，画完需按任意键才会显示结果

import cv2
import numpy as np

current_pos = None
tl = None
br = None


# 鼠标事件
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
    return tl, br   # tl=(y1,x1), br=(y2,x2)


# 读取摄像头/视频，然后用鼠标事件画框
def readVideo(pathName, skipFrame):  # pathName为视频文件路径，skipFrame为视频的第skipFrame帧

    cap = cv2.VideoCapture(0)  # 读取摄像头
    if not cap.isOpened():  # 如果未发现摄像头，则按照路径pathName读取视频文件
        cap = cv2.VideoCapture(pathName)  # 读取视频
    c = 1
    while True:
        ret, frame = cap.read()
        if ret:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            if c == skipFrame:
                (a, b) = get_rect(frame, title='get_rect')  # 鼠标画矩形框

            cv2.imshow('frame', frame)
            c += 1
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    cap.release()
    cv2.destroyAllWindows()


readVideo("examples/video/56.mp4", 1)


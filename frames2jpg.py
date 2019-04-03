# -*- coding: utf-8 -*-

# Process the video stream into a picture frame by frame
# the pictures are used by Video_Object_Tracking.py

import cv2

vc = cv2.VideoCapture("examples/video/test.mp4")  # 读入视频文件
c = 0
rval = vc.isOpened()

while rval:   # 循环读取视频帧
    c += 1
    rval, frame = vc.read()
    if rval:
        cv2.imwrite("examples/video_frames/" + str(c) + '.jpg', frame)  # 存储为图像,保存名为数字.jpg
        cv2.waitKey(1)
    else:
        break
vc.release()
print('save_success')
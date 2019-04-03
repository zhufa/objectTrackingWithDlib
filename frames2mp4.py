# -*- coding: utf-8 -*-

# 将处理后的帧继续保存为视频
# 参考 https://blog.csdn.net/zj360202/article/details/79026891

import cv2

vc = cv2.VideoCapture("examples/video/test.mp4")  # 读入视频文件
c = 0
rval = vc.isOpened()
fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')

# fourcc = cv2.VideoWriter_fourcc(*'XVID') 用来保存avi文件

fps = 30
size = (int(vc.get(cv2.CAP_PROP_FRAME_WIDTH)), int(vc.get(cv2.CAP_PROP_FRAME_HEIGHT)))
out = cv2.VideoWriter('camera_test.mp4', fourcc, fps, size)

while rval:   # 循环读取视频帧
    c += 1
    rval, frame = vc.read()
    if rval:
        # 写入一帧
        out.write(frame)
    else:
        break
vc.release()
out.release()
print('save_success')

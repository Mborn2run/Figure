import cv2
import time
import os
import numpy as np

counter = 1
AUTO = True  # 自动拍照，或手动按s键拍照
INTERVAL = 2 # 自动拍照间隔
# 左相机是2，右相机是1
camera = cv2.VideoCapture(1)

# 读取当前摄像头的分辨率
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 2560)#设置分辨率
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)#
width = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))

print("摄像头分辨率: {} x {}".format(width, height))

utc = time.time()
folder = "G:\\learning_materials\\stereo_camera\\pictures" # 拍照文件目录G:\learning_materials\bi_camera_pictures

def shot(frame_L,frame_R):
    global counter
    leftpath = os.path.join(folder, "left", f"left_{counter}.jpg")
    rightpath = os.path.join(folder, "right", f"right_{counter}.jpg")
    leftframe=frame_L
    rightframe=frame_R
    cv2.imwrite(leftpath, leftframe)

    cv2.imwrite(rightpath, rightframe)
    print("snapshot saved into: " + leftpath)
    print("snapshot saved into: " + rightpath)

while True:
    ret, frame = camera.read()

    # 获取帧的宽度和高度
    frame_width = frame.shape[1]
    frame_height = frame.shape[0]

    # 将帧分割为左右两个图像
    half_width = frame_width // 2
    left_frame = frame[:, :half_width, :]
    right_frame = frame[:, half_width:, :]

    # 显示左右图像
    cv2.imshow('Left Frame', left_frame)
    cv2.imshow('Right Frame', right_frame)
    cv2.imshow('Image', frame)


    now = time.time()
    key = cv2.waitKey(1)
    if key == ord("q"):
        break
    elif key == ord("s"):
        shot(left_frame,right_frame)
        counter += 1

camera.release()
cv2.destroyWindow("Left Frame")
cv2.destroyWindow("Right Frame")
cv2.destroyWindow("Image")
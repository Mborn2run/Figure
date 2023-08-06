
import cv2
# 原始图像读取
image = cv2.imread("assets/iron.jpg")
# 获取原始图像宽高
height, width = image.shape[0], image.shape[1]

image_resize = cv2.resize(image, (420, 400))
# 这里image_resize用来盛放修改后的结果，

# 将image_resize写入jpg格式的文件
import os
cv2.imwrite('assets/iron1.jpg', image_resize)

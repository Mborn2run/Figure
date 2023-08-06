import sys
import os

module_dir = os.path.dirname(__file__)
project_dir = os.path.abspath(os.path.join(module_dir, ".."))
sys.path.append(project_dir)

from camera import Camera
from threading import Thread

def parse_string(input_string):
    groups = input_string.split(',')  # 按逗号分割字符串为不同组
    
    front_list = []  # 存储冒号前面的数
    back_list = []  # 存储冒号后面的数
    
    for group in groups:
        key, value = group.split(':')  # 按冒号拆分每组数据
        print(key, int(value))
    
    return front_list, back_list

# # 示例用法
# input_string = input('请输入字符串: ')
# front, back = parse_string(input_string)

cameras={}
detector = None
while True:
        '''servo部分'''
        controller = input("请输入指令：")
        if controller == 'camera_on':
            open_index = input("请输入摄像头编号：")
            camera = Camera(int(open_index))
            camera_thread = Thread(target=camera.open_camera)
            camera_thread.start()
            cameras[open_index] = (camera, camera_thread)

        if controller == 'camera_off':
            close_index = input("请输入摄像头编号：")
            if close_index in cameras:
                camera, camera_thread = cameras[close_index]
                camera.change_state(False)
                camera_thread.join()
                camera = None
                del cameras[close_index]
                # cv2.destroyWindow(f"Camera {close_index}")
                print(f"Camera {close_index} is turned off.")
            else:
                print(f"Camera {close_index} is not found.")

        if controller == 'distance_on':
            if detector is None and cameras == {}:
                video_index = input("请输入摄像头编号：")
                camera = Camera(0)
                distance_thread = Thread(target=camera.calculate_distance, args=((int(video_index),)))
                distance_thread.start()
            else:
                print("存在任务冲突，不能读取距离信息")
        if controller == 'distance_off':
            if distance_thread.is_alive():
                camera.change_flag(False)
                distance_thread.join()
                camera = None
            else:
                print("距离检测线程已结束")
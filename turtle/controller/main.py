from sensor import ReadSensor
from threading import Thread
from detector import Detector
from move import Motion
from sensor import ReadSensor
from camera import Camera
from puller import Puller

'''
 1. 运动模块
 w : 向前游, s : 向后游, a : 向左游, d : 向右游
 q : 上浮, e : 下潜
 i : 向前爬, k : 复位, j : 向左爬, l : 向右爬
 u : 收wifi, o : 放wifi

 2. 功能模块
 camera_on : 打开摄像头, camera_off : 关闭摄像头
 detect_on : 打开目标检测, detect_off : 关闭目标检测
 distance_on : 打开距离检测, distance_off : 关闭距离检测
    
 exit : 退出
'''


def drawController():
    print("╔══════════════════════════════════════════════════════════════════════════════════════╗")
    print("║                                                                                      ║")
    print("║     [^]                                                                              ║")
    print("║  [<][-][>]                                                   ____                    ║")
    print("║     [v]                    ╔══╗                            /      \                  ║")
    print("║                            ║◉  ║ ◉                        /  o    o\                 ║")
    print("║                            ╚══╝                          /    __    \                ║")
    print("║           ^                                             /    /  \    \               ║")
    print("║          ^^^                                           /    /    \    \              ║")
    print("║         ^^^^^              ╔══╗                        \   \      |   /              ║")
    print("║      <<[-----]>>           ║◉  ║ ◉                      \   \     |  /               ║")
    print("║  <<<<<<[-----]>>>>>>       ╚══╝                          \   \    | /                ║")
    print("║      <<[-----]>>                                          \___\__/                   ║")
    print("║         vvvvvv                                                                       ║")
    print("║          vvv                                                                         ║")
    print("║           v                              ##                                          ║")
    print("║     [<]       [>]                       ####                                         ║")
    print("║     [<]       [>]                        ##                                          ║")
    print("║                                                                                      ║")
    print("╚══════════════════════════════════════════════════════════════════════════════════════╝")

if __name__ == '__main__':
    detector = None
    motion = Motion()
    sensor = ReadSensor()
    cameras = {}
    puller = Puller()
    while True:
        drawController()
        '''servo部分'''
        controller = input("请输入指令：")
        if controller == 'w':
            operation_time = input("请输入swim间隔时间：")
            swim_thread = Thread(target=motion.swim, args=(float(operation_time),))
            swim_thread.start()
        if controller == 'a':
            operation_time = input("请输入左转间隔时间：")
            left_thread = Thread(target=motion.swim_left, args=(float(operation_time),))
            left_thread.start()
        if controller == 'd':
            operation_time = input("请输入右转间隔时间：")
            right_thread = Thread(target=motion.swim_right, args=(float(operation_time),))
            right_thread.start()
        # if controller == 's':
        #     userdefined = input("请输入自定义舵机号，角度：")
        #     motion.userDefined(userdefined)
        if controller == 's':
            motion.swim_init()
        if controller == 'q':
            operation_time = input("请输入排水的时间：")
            puller.forward(float(operation_time))
        if controller == 'e':
            operation_time = input("请输入抽水的时间：")
            puller.backward(float(operation_time))
        if controller == 'i':
            gap_time = input("请输入间隔时间：")
            crawl_thread = Thread(target=motion.crawl_20, args=(float(gap_time),))
            crawl_thread.start()
        if controller == 'k':
            motion.crawl_init()
        if controller == 'j':
            gap_time = input("请输入间隔时间：")
            crawl_thread = Thread(target=motion.crawl_left, args=(float(gap_time),))
            crawl_thread.start()
        if controller == 'l':
            gap_time = input("请输入间隔时间：")
            crawl_thread = Thread(target=motion.crawl_right, args=(float(gap_time),))
            crawl_thread.start()
        if controller == 'u':
            op_time = input("请输入顺时针运动时间：")
            motion.wifi(int(op_time), 0)
        if controller == 'o':
            op_time = input("请输入逆时针运动时间：")
            motion.wifi(int(op_time), 1)

        '''detector部分'''
        if controller == 'detector_on':
            detector_index = input("请输入摄像头编号：")
            if detector is None:
                detector = Detector(int(detector_index))
                detector.setFlag(True)
                detector_thread = Thread(target=detector.run)
                detector_thread.start()
            else:
                print("detector对象已存在")

        if controller == 'detector_off':
            if detector is not None:
                detector.setFlag(False)
                detector_thread.join()
                detector = None
            else:
                print("detector对象不存在")

        '''camera部分'''
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
                print(f"Camera {close_index} is turned off.")
            else:
                print(f"Camera {close_index} is not found.")

        '''distance部分'''
        if controller == 'distance_on':
            if detector is None and cameras == {}:
                video_index = input("请输入摄像头编号：")
                camera = Camera(100)
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
        if controller == 'exit':
            break
        # if controller == 'print':
        #     if detector_thread.is_alive():
        #         print("目标检测线程仍在运行")
        #     else:
        #         print("目标检测线程已结束")
        #     if detector is None:
        #         print("detector对象不存在")
        #     else:
        #         print(detector)

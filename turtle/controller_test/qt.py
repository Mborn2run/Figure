#!/usr/bin/python3
import sys
sys.path.append('/home/pi/.local/lib/python3.7/site-packages')
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit
from PyQt5.QtGui import QPalette, QBrush, QPixmap,QColor
from threading import Thread
from camera import Camera
from detector import Detector
from move import Motion
from puller import Puller


detector = None
cameras = {}
distance_thread = None
detector_thread = None
camera_thread = None
crawl_thread = None
motion = Motion()
puller = Puller()

def servo_function():
    servo_index = str(servo_function_input.text())
    servo_function_input.clear()
    motion.userDefined(servo_index)

def push():
    operating_time = float(puller_function_input.text())
    puller_function_input.clear()
    puller.forward(float(operating_time))
    ...

def pull():
    operating_time = float(puller_function_input.text())
    puller_function_input.clear()
    puller.backward(float(operating_time))
    ...

def move_forward():
    global crawl_thread
    sleep_time = float(move_sleep_time_input.text())
    move_sleep_time_input.clear()
    crawl_thread = Thread(target=motion.crawl_left, args=(float(sleep_time),))
    crawl_thread.start()

def move_backward():
    ...

def move_left():
    ...

def move_right():
    ...

def swim_forward():
    ...

def swim_backward():
    ...

def swim_left():
    ...

def swim_right():
    ...

def wifi_in_func():
    op_time = float(wifi_sleep_time.text())
    wifi_sleep_time.clear()
    motion.wifi(int(op_time), 0)
    ...

def wifi_out_func():
    op_time = float(wifi_sleep_time.text())
    wifi_sleep_time.clear()
    motion.wifi(int(op_time), 1)
    ...

def dectect_on():
    global detector, detector_thread
    detector_index = int(detector_input.text())
    detector_input.clear()
    if detector is None:
        detector = Detector(int(detector_index))
        detector.setFlag(True)
        detector_thread = Thread(target=detector.run)
        detector_thread.start()
    else:
        print("detector对象已存在")

def detect_off():
    global detector, detector_thread
    if detector is not None:
        detector.setFlag(False)
        detector_thread.join()
        detector = None
    else:
        print("detector对象不存在")

def open_camera():
    global cameras, camera_thread
    camera_index = int(open_camera_input.text())
    open_camera_input.clear()

    camera = Camera(camera_index)
    camera_thread = Thread(target=camera.open_camera)
    camera_thread.start()
    cameras[camera_index] = (camera, camera_thread)

def close_camera():
    global cameras, camera_thread
    camera_index = int(close_camera_input.text())
    close_camera_input.clear()

    if camera_index in cameras:
        camera, camera_thread = cameras[camera_index]
        camera.change_state(False)
        camera_thread.join()
        camera = None
        del cameras[camera_index]

def distance_on():
    global camera, distance_thread, detector
    camera_index = int(distance_input.text())
    distance_input.clear()

    if detector is None and cameras == {}:
        camera = Camera(0)
        distance_thread = Thread(target=camera.calculate_distance, args=((int(camera_index),)))
        distance_thread.start()
    else:
        print("存在任务冲突，不能读取距离信息")

def distance_off():
    global camera, distance_thread
    if distance_thread.is_alive():
        camera.change_flag(False)
        distance_thread.join()
        camera = None
    else:
        print("距离检测线程已结束")


app = QApplication(sys.argv)



# 创建窗口
window = QWidget()
window.setWindowTitle("Turtle Robot Control Panel")
# window.setGeometry(800, 300, 600, 500)
window.setGeometry(400, 100, 1200, 900)
palette = QPalette()
# palette.setBrush(QPalette.Background, QBrush(QPixmap("assets/iron_man.png")))
palette.setBrush(QPalette.Background, QBrush(QPixmap("assets/iron.jpg")))
window.setPalette(palette)

style = """
    QLabel {
        font-weight: bold;
        font-size: 16px;
        color: white;
    }
"""

# 创建布局
main_layout = QVBoxLayout()
servo_layout = QHBoxLayout()
puller_layout = QHBoxLayout()
wifi_layout = QHBoxLayout()
move_layout = QHBoxLayout()
swim_layout = QHBoxLayout()
detector_layout = QHBoxLayout()
open_camera_layout = QHBoxLayout()
close_camera_layout = QHBoxLayout()
distance_layout = QHBoxLayout()

# 创建自定义舵机转动部分的组件
servo_function_label = QLabel("Servo Control:")
servo_function_label.setStyleSheet(style)
servo_function_input = QLineEdit()
servo_function_input.setPlaceholderText("choose servo:")
servo_function_button = QPushButton("run")

servo_function_button.clicked.connect(servo_function)

servo_layout.addWidget(servo_function_label)
servo_layout.addWidget(servo_function_input)
servo_layout.addWidget(servo_function_button)

# 创建自定义推杆电机部分的组件
puller_function_label = QLabel("Puller Control:")
puller_function_label.setStyleSheet(style)
puller_function_input = QLineEdit()
puller_function_input.setPlaceholderText("input operating time:")
push_button = QPushButton("推")
pull_button = QPushButton("拉")

push_button.clicked.connect(push)
pull_button.clicked.connect(pull)

puller_layout.addWidget(puller_function_label)
puller_layout.addWidget(puller_function_input)
puller_layout.addWidget(push_button)
puller_layout.addWidget(pull_button)

# 创建wifi部分的组件
wifi_label = QLabel("Wifi Control:")
wifi_label.setStyleSheet(style)
wifi_sleep_time = QLineEdit()
wifi_sleep_time.setPlaceholderText("input wifi name:")
wifi_in = QPushButton("收wifi")
wifi_out = QPushButton("放wifi")

wifi_in.clicked.connect(wifi_in_func)
wifi_out.clicked.connect(wifi_out_func)

wifi_layout.addWidget(wifi_label)
wifi_layout.addWidget(wifi_sleep_time)
wifi_layout.addWidget(wifi_in)
wifi_layout.addWidget(wifi_out)


# 创建运动部分的组件
move_label = QLabel("Move Control:")
move_label.setStyleSheet(style)
move_sleep_time_input = QLineEdit()
move_sleep_time_input.setPlaceholderText("input sleep time:")
forward_button = QPushButton("Forward")
backward_button = QPushButton("Backward")
left_button = QPushButton("Left")
right_button = QPushButton("Right")

forward_button.clicked.connect(move_forward)
backward_button.clicked.connect(move_backward)
left_button.clicked.connect(move_left)
right_button.clicked.connect(move_right)

move_layout.addWidget(move_label)
move_layout.addWidget(move_sleep_time_input)
move_layout.addWidget(forward_button)
move_layout.addWidget(backward_button)
move_layout.addWidget(left_button)
move_layout.addWidget(right_button)

# 创建游泳部分的组件
swim_label = QLabel("Swim Control:")
swim_label.setStyleSheet(style)
swim_sleep_time_input = QLineEdit()
swim_sleep_time_input.setPlaceholderText("input sleep time:")
swim_forward_button = QPushButton("Forward")
swim_backward_button = QPushButton("Backward")
swim_left_button = QPushButton("Left")
swim_right_button = QPushButton("Right")

swim_forward_button.clicked.connect(swim_forward)
swim_backward_button.clicked.connect(swim_backward)
swim_left_button.clicked.connect(swim_left)
swim_right_button.clicked.connect(swim_right)

swim_layout.addWidget(swim_label)
swim_layout.addWidget(swim_sleep_time_input)
swim_layout.addWidget(swim_forward_button)
swim_layout.addWidget(swim_backward_button)
swim_layout.addWidget(swim_left_button)
swim_layout.addWidget(swim_right_button)



# 创建打开目标检测的组件
detector_label = QLabel("Target Detection:")
detector_label.setStyleSheet(style)
detector_input = QLineEdit()
detector_input.setPlaceholderText("Enter detector index")
detector_on_button = QPushButton("Turn On")

detector_on_button.clicked.connect(dectect_on)

detector_layout.addWidget(detector_label)
detector_layout.addWidget(detector_input)
detector_layout.addWidget(detector_on_button)

# 创建关闭目标检测的组件
detector_off_button = QPushButton("Turn Off")

detector_off_button.clicked.connect(detect_off)

detector_layout.addWidget(detector_off_button)

# 创建打开摄像头部分的组件
open_camera_label = QLabel("Open Camera:")
open_camera_label.setStyleSheet(style)
open_camera_input = QLineEdit()
open_camera_input.setPlaceholderText("Enter camera index")
open_camera_button = QPushButton("Open")

open_camera_button.clicked.connect(open_camera)

open_camera_layout.addWidget(open_camera_label)
open_camera_layout.addWidget(open_camera_input)
open_camera_layout.addWidget(open_camera_button)

# 创建关闭摄像头部分的组件
close_camera_label = QLabel("Close Camera:")
close_camera_label.setStyleSheet(style)
close_camera_input = QLineEdit()
close_camera_input.setPlaceholderText("Enter camera index")
close_camera_button = QPushButton("Close")

close_camera_button.clicked.connect(close_camera)

close_camera_layout.addWidget(close_camera_label)
close_camera_layout.addWidget(close_camera_input)
close_camera_layout.addWidget(close_camera_button)

# 创建打开距离检测的组件
distance_label = QLabel("Distance Detection:")
distance_label.setStyleSheet(style)
distance_input = QLineEdit()
distance_input.setPlaceholderText("Enter distance index")
distance_on_button = QPushButton("Turn On")

distance_on_button.clicked.connect(distance_on)

distance_layout.addWidget(distance_label)
distance_layout.addWidget(distance_input)
distance_layout.addWidget(distance_on_button)

# 创建关闭距离检测的组件
distance_off_button = QPushButton("Turn Off")

distance_off_button.clicked.connect(distance_off)

distance_layout.addWidget(distance_off_button)

# 添加布局到主布局
main_layout.addLayout(servo_layout)
main_layout.addLayout(puller_layout)
main_layout.addLayout(move_layout)
main_layout.addLayout(swim_layout)
main_layout.addLayout(wifi_layout)
main_layout.addLayout(detector_layout)
main_layout.addLayout(open_camera_layout)
main_layout.addLayout(close_camera_layout)
main_layout.addLayout(distance_layout)

# 设置主布局
window.setLayout(main_layout)


window.show()
sys.exit(app.exec_())

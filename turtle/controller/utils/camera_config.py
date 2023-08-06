import cv2
import numpy as np
 
# 左镜头的内参，如焦距
left_camera_matrix = np.array([[671.547208740291,0,0],
[-0.416323772777705,671.355269240587,0],
[604.190314450856,377.289737064780,1]])
left_camera_matrix = np.transpose(left_camera_matrix)
right_camera_matrix = np.array([[6.718176573422229e+02,0,0.],[-1.106787265314457,6.711163877161091e+02,0.],[6.230582262720928e+02,3.688635325000979e+02,1.]])
right_camera_matrix = np.transpose(right_camera_matrix)

# 畸变系数,K1、K2、K3为径向畸变,P1、P2为切向畸变
left_distortion = np.array([[-0.064970304210746,-0.020157302109384,-0.001110421651486,0.001138942126735]])
right_distortion = np.array([[-0.062633913776927,-0.032370379436617,-8.465390454050292e-04,-0.001065905496957]])

# 旋转矩阵
R = np.array([[0.999969956158676,-0.001408803712639,0.007622470210812],[0.001418476877669,0.999998195395827,-0.001263775469404],[-0.007620676043697,0.001274549798479,0.999970149964212]])
R = np.transpose(R)
# 平移矩阵
T = np.array([-61.398436211540010,0.054790360825853,-0.244215862158183])

size = (640, 480)
 
R1, R2, P1, P2, Q, validPixROI1, validPixROI2 = cv2.stereoRectify(left_camera_matrix, left_distortion,
                                                                  right_camera_matrix, right_distortion, size, R,
                                                                  T)
 
left_map1, left_map2 = cv2.initUndistortRectifyMap(left_camera_matrix, left_distortion, R1, P1, size, cv2.CV_16SC2)
right_map1, right_map2 = cv2.initUndistortRectifyMap(right_camera_matrix, right_distortion, R2, P2, size, cv2.CV_16SC2)
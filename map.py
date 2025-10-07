import math
import numpy as np

def pixel_to_map(u, v, d, gimbal_yaw_deg, gimbal_pitch_deg, gimbal_pos, fx=205.47, fy=205.47, cx=320.5, cy=180.5):
    """
    基于三角几何将图像中的像素点转换到map坐标系（ENU）
    """
    # 将角度转换为弧度
    yaw = math.radians(gimbal_yaw_deg)
    pitch = math.radians(gimbal_pitch_deg)
    
    # 计算目标相对于相机的水平角度和垂直角度
    A = math.atan2(-u + cx, fx)  # 水平角度
    B = math.atan2(-v + cy, fy)  # 垂直角度
    
    # 计算目标在相机坐标系中的方向向量
    # 使用球坐标到笛卡尔坐标的转换
    x_c = d * math.cos(B) * math.cos(A)
    y_c = d * math.cos(B) * math.sin(A)
    z_c = d * math.sin(B)
    
    # 将相机坐标系中的点转换到世界坐标系
    # 考虑云台的yaw和pitch
    
    # 首先，应用pitch旋转（绕y轴）
    x_pitched = x_c * math.cos(pitch) - z_c * math.sin(pitch)
    y_pitched = y_c
    z_pitched = x_c * math.sin(pitch) + z_c * math.cos(pitch)
    
    # 然后，应用yaw旋转（绕z轴）
    x_rotated = x_pitched * math.cos(yaw) - y_pitched * math.sin(yaw)
    y_rotated = x_pitched * math.sin(yaw) + y_pitched * math.cos(yaw)
    z_rotated = z_pitched
    
    # 加上云台位置
    x_m = x_rotated + gimbal_pos[0]
    y_m = y_rotated + gimbal_pos[1]
    z_m = z_rotated + gimbal_pos[2]
    
    return x_m, y_m, z_m

# 测试用例
test_u = 320.5  # cx
test_v = 180.5  # cy
test_d = 10.0   # 10米距离
test_pos = (0, 0, 10)  # 云台在(0,0,10)

# # 测试1: 水平指向
# test_yaw1 = 0
# test_pitch1 = 0
# result1 = pixel_to_map_corrected(test_u, test_v, test_d, test_yaw1, test_pitch1, test_pos)
# print(f"水平指向: {result1}")  # 预期: (10.0, 0.0, 10.0)

# # 测试2: 向下30度
# test_yaw2 = 0
# test_pitch2 = -30
# result2 = pixel_to_map_corrected(test_u, test_v, test_d, test_yaw2, test_pitch2, test_pos)
# print(f"向下30度: {result2}")  # 预期: (8.66, 0.0, 5.0)

# 测试用例
test_u = 320.5  # cx
test_v = 180.5  # cy
test_d = 10.0   # 10米距离
test_pos = (0, 0, 10)  # 云台在(0,0,10)

# 测试1: 水平指向
test_yaw1 = 0
test_pitch1 = 0
result1 = pixel_to_map(test_u, test_v, test_d, test_yaw1, test_pitch1, test_pos)
print(f"水平指向: {result1}")  # 预期: (10.0, 0.0, 10.0)

# 测试2: 向下30度
test_yaw2 = 0
test_pitch2 = -30
result2 = pixel_to_map(test_u, test_v, test_d, test_yaw2, test_pitch2, test_pos)
print(f"向下30度: {result2}")  # 预期: (8.66, 0.0, 5.0)

# 测试3: 向上30度
test_yaw3 = 0
test_pitch3 = 30
result3 = pixel_to_map(test_u, test_v, test_d, test_yaw3, test_pitch3, test_pos)
print(f"向上30度: {result3}")  # 预期: (8.66, 0.0, 15.0)

# 测试4: 向右偏航30度
test_yaw4 = 30
test_pitch4 = 0
result4 = pixel_to_map(test_u, test_v, test_d, test_yaw4, test_pitch4, test_pos)
print(f"向右偏航30度: {result4}")  # 预期: (8.66, 5.0, 10.0)

# 测试5: 向下30度且向右偏航30度
test_yaw5 = 30
test_pitch5 = -30
result5 = pixel_to_map(test_u, test_v, test_d, test_yaw5, test_pitch5, test_pos)
print(f"向下30度且向右偏航30度: {result5}")  # 预期: (7.5, 4.33, 5.0)

# 测试6: 目标不在图像中心（右上角）
test_u6 = 400.5  # 右上角
test_v6 = 180.5   # 右上角
test_yaw6 = 0
test_pitch6 = 0
result6 = pixel_to_map(test_u6, test_v6, test_d, test_yaw6, test_pitch6, test_pos)
print(f"目标在右上角: {result6}")  # 预期: (x>10, y<0, z>10)

# 测试7: 目标不在图像中心（左下角）
test_u7 = 220.5  # 左下角
test_v7 = 280.5  # 左下角
test_yaw7 = 0
test_pitch7 = 0
result7 = pixel_to_map(test_u7, test_v7, test_d, test_yaw7, test_pitch7, test_pos)
print(f"目标在左下角: {result7}")  # 预期: (x<10, y>0, z<10)
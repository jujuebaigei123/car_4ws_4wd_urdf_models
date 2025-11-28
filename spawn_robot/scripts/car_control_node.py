#!/usr/bin/env python
import numpy as np
import geometry_msgs
import rospy
import math
from geometry_msgs.msg import Twist
from std_msgs.msg import Float64

# ==========================================================
# 该控制器为前后轮同步转向的阿克曼控制器
# ==========================================================
class FourWSCarController:
    def __init__(self):
        rospy.init_node('four_ws_car_controller', anonymous=True)
        
        # 订阅 /cmd_vel 指令
        rospy.Subscriber('/cmd_vel', Twist, self.cmd_vel_callback)
        # 车辆参数
        self.WHEEL_RADIUS = 0.13  # 车轮半径 
        self.W = 0.47        # 轮距 (左右轮中心的距离)
        self.L = 0.64        # 轴距 (前后轮中心的距离)
        self.MAX_SPEED = 2   # m/s,最大速度
        self.MAX_STEER_ANGLE = 0.39 # 最大转向控制量0.39rad,保证解算后最大轮转角不超URDF中定义的limit 0.55rad
        
        # 定义 8 个控制器发布器 (请确保命名空间和话题与你的 Launch 文件一致)
        namespace = '/car_4ws_4wd'
        self.pub_steer = {
            'fl': rospy.Publisher(namespace + '/fl_steer_controller/command', Float64, queue_size=1),
            'fr': rospy.Publisher(namespace + '/fr_steer_controller/command', Float64, queue_size=1),
            'rl': rospy.Publisher(namespace + '/rl_steer_controller/command', Float64, queue_size=1),
            'rr': rospy.Publisher(namespace + '/rr_steer_controller/command', Float64, queue_size=1),
        }
        self.pub_drive = {
            'fl': rospy.Publisher(namespace + '/fl_drive_controller/command', Float64, queue_size=1),
            'fr': rospy.Publisher(namespace + '/fr_drive_controller/command', Float64, queue_size=1),
            'rl': rospy.Publisher(namespace + '/rl_drive_controller/command', Float64, queue_size=1),
            'rr': rospy.Publisher(namespace + '/rr_drive_controller/command', Float64, queue_size=1),
        }

        rospy.loginfo("4WS/4WD Car Controller Initialized.")

    def cmd_vel_callback(self, msg:Twist):
        linear_x = msg.linear.x
        angular_z = msg.angular.z
        # 限幅
        linear_x = np.clip(linear_x, -self.MAX_SPEED, self.MAX_SPEED)
        angular_z = np.clip(angular_z, -self.MAX_STEER_ANGLE, self.MAX_STEER_ANGLE)
        
        delta_z_safe = angular_z + 1e-8     # 防止除0
        R = (self.L / 2) / abs(math.tan(delta_z_safe))   # 转弯半径
        omega = linear_x / R

        # 内外轮转角和半径
        delta_near = math.atan((self.L / 2) / (R - self.W / 2))
        delta_far  = math.atan((self.L / 2) / (R + self.W / 2))
        dis_near   = math.sqrt((R - self.W / 2) ** 2 + (self.L / 2) ** 2)
        dis_far    = math.sqrt((R + self.W / 2) ** 2 + (self.L / 2) ** 2)

        # 左转 or 右转
        if angular_z > 0:
            v_fl = dis_near * omega / self.WHEEL_RADIUS
            v_fr = dis_far * omega / self.WHEEL_RADIUS
            delta_fl = delta_near
            delta_fr = delta_far
        else:
            v_fl = dis_far * omega / self.WHEEL_RADIUS
            v_fr = dis_near * omega / self.WHEEL_RADIUS
            delta_fl = -delta_far
            delta_fr = -delta_near
        # 后轮
        v_rl, v_rr = v_fl, v_fr
        delta_rl, delta_rr = -delta_fl, -delta_fr

        # 直线情况覆盖
        if abs(angular_z) < 1e-4:
            straight_v = linear_x / self.WHEEL_RADIUS
            v_fl = v_fr = v_rl = v_rr = straight_v
            delta_fl = delta_fr = delta_rl = delta_rr = 0.0
        # 发布驱动命令
        self._publish_steer_commands(delta_fl, delta_fr, delta_rl, delta_rr)
        self._publish_drive_commands(v_fl, v_fr, v_rl, v_rr)

    def _publish_steer_commands(self, fl, fr, rl, rr):
        self.pub_steer['fl'].publish(Float64(fl))
        self.pub_steer['fr'].publish(Float64(fr))
        self.pub_steer['rl'].publish(Float64(rl))
        self.pub_steer['rr'].publish(Float64(rr))
        
    def _publish_drive_commands(self, fl, fr, rl, rr):
        self.pub_drive['fl'].publish(Float64(fl))
        self.pub_drive['fr'].publish(Float64(fr))
        self.pub_drive['rl'].publish(Float64(rl))
        self.pub_drive['rr'].publish(Float64(rr))

if __name__ == '__main__':
    try:
        controller = FourWSCarController()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
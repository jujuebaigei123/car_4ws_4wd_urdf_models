# car_4ws_4wd_urdf_models
四轮驱动四轮转向小车urdf模型及solidworks模型
## 简单测试
### 基础模型测试
1. 创建工作空间：`mkdir -p urdf_test/src`
2. 将car_4ws_4wd复制到创建的src目录下
3. 在工作空间根目录下编译并source工作空间
4. 运行launch：`roslaunch car_4ws_4wd display.launch`
   可以使用rqt工具检查模型关节转动状态
### Gazebo控制测试
1. 将spawn_robot复制到创建的src目录下
2. 在工作空间根目录下编译并source工作空间
3. 运行launch：`roslaunch spawn_robot run_all.launch`
   运行后有4辆车均可以单独控制，话题名称为`/robot_{i}/four_wheel_steering_controller/cmd_vel`



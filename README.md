# car_4ws_4wd_urdf_models
四轮驱动四轮转向小车urdf模型及solidworks模型
## 简单测试
### 基础模型测试
1. 创建工作空间：`mkdir -p urdf_test/src`
2. 将car_4ws_4wd复制到创建的src目录下
3. 在工作空间根目录下编译并source工作空间
4. 运行launch：`roslaunch car_4ws_4wd display.launch`
### Gazebo控制测试
gazebo使用的是添加控制器后的urdf文件，名称为`car_4ws_4wd_gazebo.urdf`注意和原始文件区分
1. 将spawn_robot复制到创建的src目录下
2. 在工作空间根目录下编译并source工作空间
3. 运行launch：`roslaunch spawn_robot spawn_robot.launch`
4. 使用rqt工具向`cmd_vel`发送控制指令



# car_4ws_4wd_urdf_models
四轮驱动四轮转向小车urdf模型及solidworks模型
## 简单测试

1. 创建工作空间：`mkdir -p urdf_test/src`
2. 将car_4ws_4wd解压至刚创建的src目录下
3. 编译并source工作空间
4. 运行launch：`roslaunch car_4ws_4wd display.launch`

## 注意事项

1. 该urdf仅完成基础形状及关节配置，若需要在gezebo中控制需自己添加控制器

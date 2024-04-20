# TinyMonitor

简单的性能监控程序。

# 安装

## 方式一

直接在[release](https://github.com/TikaFlow/tika_grocery/releases)中下载可执行文件。

## 方式二

在有`Python`环境时直接运行`.py`脚本。

```powershell
python monitor.py
```

# 使用

- 拖动悬浮窗到任意位置，将自动贴边。
- 左键点击托盘图标切换是否开启鼠标穿透，鼠标穿透时无法拖动悬浮窗。
- 右键点击托盘图标打开设置菜单，可以临时隐藏悬浮窗以及设置哪些信息展示。

# 打包

## #1、安装打包工具

```powershell
pip install pyinstaller
```

## #2、打包

```powershell
pyinstaller monitor.spec
```
from PyQt5 import QtWidgets, QtGui, QtCore
import pkg_resources

class TrayIcon:
    def __init__(self, parent):
        self.parent = parent
        self.mouse_transparency = True
        self.init_tray_icon()

    def init_tray_icon(self):
        # 获取图标资源文件
        icon_path = pkg_resources.resource_filename(__name__, 'static/img/icon.ico')
        self.tray_icon = QtWidgets.QSystemTrayIcon(self.parent)
        self.tray_icon.setIcon(QtGui.QIcon(icon_path))
        self.tray_icon.setToolTip("tinyMonitor - simple performance monitor")
        
        self.show_action = QtWidgets.QAction("隐藏", self.parent)
        self.show_action.triggered.connect(self.toggle_window_visibility)
        
        # 创建一个映射，将动作文本映射到父窗口的属性
        toggles = {
            "CPU": "show_cpu",
            "MEM": "show_mem",
            "上行": "show_up",
            "下行": "show_down",
        }
        
        tray_menu = QtWidgets.QMenu()
        tray_menu.addAction(self.show_action)

        # 循环添加菜单项并连接到同一个处理函数
        for text, attr in toggles.items():
            action = QtWidgets.QAction(text, self.parent)
            action.setCheckable(True)
            action.setChecked(True)
            # 使用partial来传递额外的参数
            action.triggered.connect(lambda checked, attr=attr: setattr(self.parent, attr, checked))
            tray_menu.addAction(action)
        
        quit_action = QtWidgets.QAction("退出", self.parent)
        quit_action.triggered.connect(QtWidgets.qApp.quit)
        tray_menu.addAction(quit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.on_tray_actived)
        self.tray_icon.show()

    def on_tray_actived(self, reason):
        if reason == QtWidgets.QSystemTrayIcon.Trigger:
            self.parent.toggle_penetrate(self.mouse_transparency)
            self.mouse_transparency = not self.mouse_transparency
            self.tray_icon.showMessage("提示", "鼠标穿透已{}".format("开启" if self.mouse_transparency else "关闭"), QtWidgets.QSystemTrayIcon.Information, 2000)

    def toggle_window_visibility(self):
        if self.parent.isVisible():
            self.parent.hide()
            self.show_action.setText("显示")
        else:
            self.parent.show()
            self.show_action.setText("隐藏")
            
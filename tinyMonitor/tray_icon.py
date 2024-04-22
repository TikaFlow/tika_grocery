import pkg_resources
from PyQt5.QtWidgets import QSystemTrayIcon, QAction, QMenu, qApp
from PyQt5.QtGui import QIcon

class TrayIcon:
    def __init__(self, parent):
        self.parent = parent
        self.mouse_transparency = True
        self.init_tray_icon()

    def init_tray_icon(self):
        # 获取图标资源文件
        icon_path = pkg_resources.resource_filename(__name__, 'static/img/icon.ico')
        self.tray_icon = QSystemTrayIcon(self.parent)
        self.tray_icon.setIcon(QIcon(icon_path))
        self.tray_icon.setToolTip("tinyMonitor - simple performance monitor")
        
        self.show_action = QAction("隐藏", self.parent)
        self.show_action.triggered.connect(self.toggle_window_visibility)
        
        # 创建一个映射，将动作文本映射到父窗口的属性
        toggles = {
            "CPU": "cpu",
            "MEM": "mem",
            "上行": "up",
            "下行": "down",
        }
        
        tray_menu = QMenu()
        tray_menu.addAction(self.show_action)

        # 循环添加菜单项并连接到同一个处理函数
        for text, attr in toggles.items():
            action = QAction(text, self.parent)
            action.setCheckable(True)
            action.setChecked(True)
            # 使用partial来传递额外的参数
            action.triggered.connect(lambda checked, attr=attr: self.toggle_show_info(attr, checked))
            tray_menu.addAction(action)
        
        quit_action = QAction("退出", self.parent)
        quit_action.triggered.connect(qApp.quit)
        tray_menu.addAction(quit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.on_tray_actived)
        self.tray_icon.show()

    def on_tray_actived(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            self.parent.toggle_penetrate(self.mouse_transparency)
            self.mouse_transparency = not self.mouse_transparency
            self.tray_icon.showMessage("提示", "鼠标穿透已{}".format("开启" if self.mouse_transparency else "关闭"), QSystemTrayIcon.Information, 2000)

    def toggle_show_info(self, attr, checked):
        self.parent.info_dict[attr] = checked

        if checked:
            self.parent.info_deque.append(attr)
        else:
            idx = self.parent.info_deque.index(attr)
            self.parent.info_deque.pop(idx)

    def toggle_window_visibility(self):
        if self.parent.isVisible():
            self.parent.hide()
            self.show_action.setText("显示")
        else:
            self.parent.show()
            self.show_action.setText("隐藏")
            
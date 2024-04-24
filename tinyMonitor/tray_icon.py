from PyQt5.QtWidgets import QSystemTrayIcon, QAction, QMenu, qApp
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTimer
import rcc

class TrayIcon:
    def __init__(self, parent):
        self.parent = parent
        self.init_tray_icon()

    def init_tray_icon(self):
        icon_path = ":/icons/app_icon"
        self.tray_icon = QSystemTrayIcon(self.parent)
        self.tray_icon.setIcon(QIcon(icon_path))
        self.tray_icon.setToolTip("tinyMonitor - simple performance monitor")
        
        tray_menu = QMenu()
        
        self.show_action = QAction("隐藏", self.parent)
        self.show_action.triggered.connect(self.toggle_window_visibility)
        tray_menu.addAction(self.show_action)
        
        # 创建一个映射，将动作文本映射到父窗口的属性
        toggles = {
            "CPU": "cpu",
            "MEM": "mem",
            "上行": "up",
            "下行": "down",
        }

        # 循环添加菜单项
        for text, attr in toggles.items():
            action = QAction(text, self.parent)
            action.setCheckable(True)
            action.setChecked(True)
            action.triggered.connect(lambda checked, attr=attr: self.toggle_show_info(attr, checked))
            tray_menu.addAction(action)
        
        self.movable_action = QAction("启用拖拽", self.parent)
        self.movable_action.triggered.connect(self.toggle_movable)
        tray_menu.addAction(self.movable_action)
        
        quit_action = QAction("退出", self.parent)
        quit_action.triggered.connect(self.on_exit)
        tray_menu.addAction(quit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

    def toggle_movable(self):
        flag = self.parent.toggle_penetrate()
        self.tray_icon.showMessage("提示", "鼠标穿透已{}，拖拽已{}".format("开启" if flag else "关闭", "启用" if not flag else "禁用"), QSystemTrayIcon.Information, 2000)
        self.movable_action.setText("启用拖拽" if flag else "鼠标穿透")

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

    def on_exit(self):
        self.tray_icon.showMessage("提示", "程序已退出", QSystemTrayIcon.Information, 1000)
        timer = QTimer(self.tray_icon)
        timer.setSingleShot(True)
        timer.timeout.connect(qApp.quit)
        timer.start(1152)

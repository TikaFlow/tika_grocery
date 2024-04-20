import datetime
import psutil
from PyQt5 import QtWidgets, QtCore
from tray_icon import TrayIcon

class SystemMonitor(QtWidgets.QWidget):
    def __init__(self):
        super(SystemMonitor, self).__init__()
        self.initUI()
        self.tray_icon = TrayIcon(self)
        self.show_cpu = True
        self.show_mem = True
        self.show_up = True
        self.show_down = True
        self.mouse_drag_pos = None
        self.init_update_info()
        self.show()  # 默认显示窗口

    def initUI(self):
        screen_geometry = QtWidgets.QApplication.desktop().availableGeometry(self)
        # 设置窗口属性
        self.setGeometry(int(screen_geometry.width() / 2), 0, 0, 0) # 顶端居中
        # 无任务栏图标、无边框、置顶、鼠标穿透
        self.setWindowFlags(QtCore.Qt.Tool | QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.WindowTransparentForInput)
        # 设置窗口背景为半透明
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setStyleSheet("""
            background-color: rgba(0, 0, 0, 0.25);
            border: 5px solid rgba(0, 0, 0, 0);;
            border-radius: 5px;
        """)

        # 创建一个合并的标签并设置样式
        now = datetime.datetime.now().strftime('%H:%M:%S')
        self.info_label = QtWidgets.QLabel(f'{now}', self)
        self.info_label.setStyleSheet("color: white; font-size: 24px;")
        self.info_label.setAutoFillBackground(False)

        # 定时器更新信息
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_info)
        self.timer.start(500)

    def toggle_penetrate(self, transparency):
        vs = self.isVisible()
        if transparency:
            self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowTransparentForInput)
        else:
            self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowTransparentForInput)
        self.setVisible(vs)

    def update_info(self):
        # 创建时间、CPU和MEM的信息字符串
        time_info = f"{datetime.datetime.now().strftime('%H:%M:%S')}"
        cpu_info = f' | CPU: {psutil.cpu_percent()}%' if self.show_cpu else ''
        mem_info = f' | MEM: {psutil.virtual_memory().percent}%' if self.show_mem else ''

        # 获取上行、下行速度
        net_info = psutil.net_io_counters()
        up_speed = f' | ↑{self.convertUnit(net_info.bytes_sent - self.bytes_sent)}' if self.show_up else ''
        down_speed = f' | ↓{self.convertUnit(net_info.bytes_recv - self.bytes_recv)}' if self.show_down else ''

        # 拼接所有信息并更新合并标签的内容
        total_info = time_info + cpu_info + mem_info + up_speed + down_speed
        self.info_label.setText(total_info)
        
        self.init_update_info(net_info)
        
    def init_update_info(self, net_info=psutil.net_io_counters()):
        self.bytes_sent = net_info.bytes_sent
        self.bytes_recv = net_info.bytes_recv

        self.info_label.adjustSize()
        self.adjustSize()

    def convertUnit(self, bps):
        bps = bps * 2
        if(bps < 1024):
            return f'{bps} B/s'
        elif(bps < 1024**2):
            return f'{bps / 1024:.2f} KB/s'
        elif(bps < 1024**3):
            return f'{bps / 1024**2:.2f} MB/s'
        else:
            return f'{bps / 1024**3:.2f} GB/s'

    def closeEvent(self, event):
        self.tray_icon.setVisible(False)
        super().closeEvent(event)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.mouse_drag_pos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() and event.buttons() == QtCore.Qt.LeftButton:
            self.move(event.globalPos() - self.mouse_drag_pos)
            event.accept()

    def moveEvent(self, event):
        # 获取屏幕的几何形状和窗口的几何形状
        screen_geometry = QtWidgets.QApplication.desktop().availableGeometry(self)
        window_geometry = self.geometry()

        # 定义一个可移动范围和吸附距离
        margin = QtCore.QMargins(0, 0, screen_geometry.right(), screen_geometry.bottom())
        adsorption = 16

        # 计算窗口的新位置
        new_geometry = window_geometry
        # 检测并调整四周的位置
        if window_geometry.left() - adsorption < margin.left():
            new_geometry.moveLeft(margin.left())
        if window_geometry.top() - adsorption < margin.top():
            new_geometry.moveTop(margin.top())
        if window_geometry.right() + adsorption > margin.right():
            new_geometry.moveRight(margin.right())
        if window_geometry.bottom() + adsorption > margin.bottom():
            new_geometry.moveBottom(margin.bottom())

        # 使用新位置移动窗口
        self.setGeometry(new_geometry)

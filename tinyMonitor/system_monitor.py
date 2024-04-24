import psutil
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QSystemTrayIcon
from PyQt5.QtCore import Qt, QMargins, QTimer
from tray_icon import TrayIcon

class SystemMonitor(QWidget):
    def __init__(self):
        super(SystemMonitor, self).__init__()
        self.initUI()

        self.mouse_drag_pos = None
        # 设置显示内容
        self.info_dict = {
            'cpu':True,
            'mem':True,
            'up':True,
            'down':True
        }
        self.info_deque = ['cpu', 'mem', 'up', 'down']
        net_info = psutil.net_io_counters()
        self.bytes_sent = net_info.bytes_sent
        self.bytes_recv = net_info.bytes_recv

    def initUI(self):
        screen_geometry = QApplication.desktop().availableGeometry(self)
        # 设置窗口属性
        self.setGeometry(int(screen_geometry.width() / 2), 0, 0, 0) # 顶端居中
        # 无任务栏图标、无边框、置顶、鼠标穿透
        self.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.WindowTransparentForInput)
        # 设置窗口背景为半透明
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("""
            background-color: rgba(0, 0, 0, 0.25);
            border: 5px solid rgba(0, 0, 0, 0);
            border-radius: 5px;
        """)
        # 设置托盘图标
        self.tray_icon = TrayIcon(self)

        # 创建一个合并的标签并设置样式
        now = datetime.now()
        self.last_time = int(now.timestamp() * 1000)
        self.info_label = QLabel(f"{now.strftime('%H:%M:%S')}", self)
        self.info_label.setStyleSheet("color: white; font-size: 24px;")
        self.info_label.setAutoFillBackground(False)
        self.info_label.setAlignment(Qt.AlignRight)

        # 定时器更新信息
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_info)
        self.timer.start(500)

        self.show()

    def toggle_penetrate(self):
        flag = False
        if self.windowFlags() & Qt.WindowTransparentForInput:
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowTransparentForInput)
        else:
            self.setWindowFlags(self.windowFlags() | Qt.WindowTransparentForInput)
            flag = True
        self.show()
        return flag

    def update_info(self):
        # 创建时间、CPU和MEM的信息字符串
        time_info = f"{datetime.now().strftime('%H:%M:%S')}"
        cpu_info = f'CPU: {psutil.cpu_percent()}%'
        mem_info = f'MEM: {psutil.virtual_memory().percent}%'

        # 获取上行、下行速度
        now = int(datetime.now().timestamp() * 1000)
        delta = now - self.last_time
        self.last_time = now
        net_info = psutil.net_io_counters()
        up_info = f'↑{self.convertUnit(delta, net_info.bytes_sent - self.bytes_sent)}'
        down_info = f'↓{self.convertUnit(delta, net_info.bytes_recv - self.bytes_recv)}'

        # 拼接所有信息并更新合并标签的内容
        total_info = self.get_total_info({
            'time':time_info, 'cpu':cpu_info, 'mem':mem_info, 'up':up_info, 'down':down_info
        })
        self.info_label.setText(total_info)
        
        self.bytes_sent = net_info.bytes_sent
        self.bytes_recv = net_info.bytes_recv

        self.info_label.adjustSize()
        self.adjustSize()

    def get_total_info(self, dict):
        # 设置合并标签的文本
        total_info = dict['time']
        quelen = len(self.info_deque)
        for i in range(quelen):
            if quelen > 2 and i == (quelen - 2):
                total_info += '\n'
            else:
                total_info += ' | '
            total_info += dict[self.info_deque[i]]

        return total_info
        
    def convertUnit(self, delta, flow):
        bps = flow * 1000 / delta
        # 转换bps为合适的单位
        if(bps < 1024):
            return f'{bps:.0f} B/s'
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
        if event.button() == Qt.LeftButton:
            self.mouse_drag_pos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() and event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.mouse_drag_pos)
            event.accept()

    def moveEvent(self, event):
        # 获取屏幕的几何形状和窗口的几何形状
        screen_geometry = QApplication.desktop().availableGeometry(self)
        window_geometry = self.geometry()

        # 定义一个可移动范围和吸附距离
        margin = QMargins(0, 0, screen_geometry.right(), screen_geometry.bottom())
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

import sys
from PyQt5.QtWidgets import QApplication
from system_monitor import SystemMonitor

if __name__ == '__main__':
    app = QApplication(sys.argv)
    monitor = SystemMonitor()
    sys.exit(app.exec_())

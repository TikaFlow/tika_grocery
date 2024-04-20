import sys
from PyQt5 import QtWidgets
from system_monitor import SystemMonitor

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    monitor = SystemMonitor()
    sys.exit(app.exec_())

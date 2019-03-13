import sys
import time

from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import pyqtSlot, Qt
from qThread import Scanner
"""
Proof of concept program scanning screen of Minecraft debugging menu using tesseract OCR
This is just window making code that displays scanned data. Fun part is in qThread.py
"""

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'MinecraftDigger'
        self.left = 0
        self.top = 0
        self.width = 320
        self.height = 200

        self.data = dict()
        self.data["Rotation"] = float(0)
        self.data['x'] = float(0)
        self.data['z'] = float(0)

        time.sleep(3)
        self.initUI()
        self.thread = Scanner()
        self.thread.refresh.connect(self.write_data)
        self.thread.start()

    def write_data(self):
        self.data["Rotation"] = self.thread.rotate
        self.data["x"] = self.thread.x
        self.data["z"] = self.thread.z
        self.refresh()

    def refresh(self):
        for name_label, label in self.labels.items():
            label.setText(name_label+": "+str(self.data[name_label]))
        self.update()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        grid = QVBoxLayout()
        self.labels = dict()
        for name_label, data in self.data.items():
            label = QLabel(name_label+": "+str(data))
            self.labels[name_label] = label
            grid.addWidget(label)
        grid.addStretch(1)
        self.setLayout(grid)

        self.show()
        self.activateWindow()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

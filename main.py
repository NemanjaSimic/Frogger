import sys
from PyQt5 import QtCore
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QImage, QPalette, QBrush
from PyQt5.QtWidgets import *
from KeyNotifier import *
from player import Player
import time
from multiprocessing import Process, Queue
from threading import Thread
from MovingCars import CarMoving

from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot


class SimMoveDemo(QWidget):

    def __init__(self):
        super().__init__()

        self.pix1 = QPixmap("frog.png")

        self.label1 = QLabel(self)
        self.label2 = QLabel(self)

        self.movingCar = CarMoving(self)

        # self.player1 = Player(self.label)
        self.__init_ui__()

        self.key_notifier = KeyNotifier()
        self.key_notifier.key_signal.connect(self.__frogMovement__)
        self.key_notifier.start()

    def __init_ui__(self):

        self.setGeometry(400, 300, 480, 600)
        self.setFixedSize(self.size())
        oImage = QImage("background.png")
        sImage = oImage.scaled(QSize(480, 600))
        palette = QPalette()
        palette.setBrush(10, QBrush(sImage))
        self.setPalette(palette)

        self.label1.setPixmap(self.pix1)
        self.label1.setGeometry(220, 560, 40, 40)

        self.setWindowTitle("Frogger")
        self.show()

    def keyPressEvent(self, event):
        self.key_notifier.add_key(event.key())

    def keyReleaseEvent(self, event):
        self.key_notifier.rem_key(event.key())
        if event.key() == Qt.Key_Right:
            self.pix1 = QPixmap("frog_right.png")
        elif event.key() == Qt.Key_Left:
            self.pix1 = QPixmap("frog_left.png")
        elif event.key() == Qt.Key_Up:
            self.pix1 = QPixmap("frog.png")
        elif event.key() == Qt.Key_Down:
            self.pix1 = QPixmap("frog_back.png")

        self.label1.setPixmap(self.pix1)

    def closeEvent(self, event):
        self.key_notifier.die()
        self.movingCar.die()

    def __frogMovement__(self, key):
        rec1 = self.label1.geometry()

        if key == Qt.Key_Right:
            self.pix1 = QPixmap("frog_right_jump.png")
            self.label1.setPixmap(self.pix1)
            self.label1.setGeometry(rec1.x() + 35, rec1.y(), rec1.width(), rec1.height())
        elif key == Qt.Key_Down:
            self.pix1 = QPixmap("frog_back_jump.png")
            self.label1.setPixmap(self.pix1)
            self.label1.setGeometry(rec1.x(), rec1.y() + 40, rec1.width(), rec1.height())
        elif key == Qt.Key_Up:
            self.pix1 = QPixmap("frog_jump.png")
            self.label1.setPixmap(self.pix1)
            self.label1.setGeometry(rec1.x(), rec1.y() - 40, rec1.width(), rec1.height())
        elif key == Qt.Key_Left:
            self.pix1 = QPixmap("frog_left_jump.png")
            self.label1.setPixmap(self.pix1)
            self.label1.setGeometry(rec1.x() - 35, rec1.y(), rec1.width(), rec1.height())
        elif key == Qt.Key_Escape:
            sys.exit(app.exec_())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = SimMoveDemo()
    sys.exit(app.exec_())

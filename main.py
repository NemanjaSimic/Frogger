import sys
from PyQt5 import QtCore
from PyQt5.QtCore import QSize,Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QImage, QPalette, QBrush
from PyQt5.QtWidgets import *
from KeyNotifier import  *
from player import Player
import time
from multiprocessing import Process,Queue
from threading import Thread
from random import *

from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot

class SimMoveDemo(QWidget):

    def __init__(self):
        super().__init__()
        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()
        self.pix1 = QPixmap("frog.png")
        self.label1 = QLabel(self)
        self.setGeometry(100, 100, 480, 600)
        self.setFixedSize(self.size())
        self.label2 = QLabel(self)
        self.lcar1 = QLabel(self)

        #self.player1 = Player(self.label)
        self.__init_ui__()

        self.key_notifier = KeyNotifier()

        self.key_notifier.key_signal.connect(self.__frogMovement__)
        self.key_notifier.start()

    def __init_ui__(self):
        self.setGeometry(400, 300, 480, 600)
        self.setWindowTitle("Frogger")
        self.label1.setGeometry(254, 258, self.pix1.height(), self.pix1.width())
        #self.setStyleSheet('background-image: url(background.png)')
        oImage = QImage("background.png")
        sImage = oImage.scaled(QSize(480, 600))
        palette = QPalette()
        palette.setBrush(10, QBrush(sImage))
        self.setPalette(palette)

        self.show()

    def keyPressEvent(self, event):
        self.key_notifier.add_key(event.key())

    def keyReleaseEvent(self, event):
         self.key_notifier.rem_key(event.key())
         self.label1.setPixmap(self.pix1)

    def __frogMovement__(self, key):
        rec1 = self.label1.geometry()

        if key == Qt.Key_Right:
            self.label1.setPixmap(self.pix1)
            self.label1.setGeometry(rec1.x() + 10, rec1.y(), rec1.width(), rec1.height())
        elif key == Qt.Key_Down:
            self.label1.setPixmap(self.pix1)
            self.label1.setGeometry(rec1.x(), rec1.y() + 25, rec1.width(), rec1.height())
        elif key == Qt.Key_Up:
            self.label1.setPixmap(self.pix1)
            self.label1.setGeometry(rec1.x(), rec1.y() - 25, rec1.width(), rec1.height())
        elif key == Qt.Key_Left:
            self.label1.setPixmap(self.pix1)
            self.label1.setGeometry(rec1.x() - 10, rec1.y(), rec1.width(), rec1.height())
        elif key == Qt.Key_Escape:
            sys.exit(app.exec_())

if __name__ == "__main__":

    app = QApplication(sys.argv)
    ex = SimMoveDemo()
    sys.exit(app.exec_())
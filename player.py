from PyQt5.QtCore import Qt, QBasicTimer, QRect, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QImage, QPalette, QBrush, QFont
from PyQt5.QtWidgets import *


class Player(QWidget):
    def __init__(self, label):
        self.label = label
        self.lives = 3
        self.score = 0
        self.stepMax = 560
        self.timer = QBasicTimer()
        self.isDead = False


    def updateLives(self):
        self.lives -= 1
        if self.lives == 0:
            self.isDead = True
            self.label.destroy()

    def updateScore(self, points):
        self.score += points

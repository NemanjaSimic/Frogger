from PyQt5.QtCore import QThread, Qt, QBasicTimer, QRect, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QImage, QPalette, QBrush, QFont
from PyQt5.QtWidgets import *
import time

SECONDS_TO_LEVEL = 30


class Player(QWidget):
    def __init__(self, label, start, score_label, lives_label, connection):
        self.label = label
        self.lives = 3
        self.score = 0
        self.stepMax = 560
        self.start = start
        self.isDead = False
        self.score_l = score_label
        self.lives_l = lives_label
        self.conn = connection

    def updateLives(self):
        self.lives -= 1
        self.lives_l.setText(str(self.lives))
        if self.lives == 0:
            self.isDead = True

    def die(self):
        self.label.destroy()

    def updateScore(self, points):
        self.score += points
        self.score_l.setText(str(self.score))

    def bonus_life(self):
        self.lives += 1
        self.lives_l.setText(str(self.lives))
        if self.lives > 0:
            self.isDead = False


class TimerClass(QThread):
    timer_signal = pyqtSignal()

    def __init__(self, parentQWidget=None):
        super(TimerClass, self).__init__(parentQWidget)
        self.parent_widget = parentQWidget

        self.was_canceled = False

    def run(self):
        while not self.was_canceled:
            self.count_time()

    def die(self):
        self.was_canceled = True

    @pyqtSlot()
    def count_time(self):
        self.parent_widget.timer -= 1
        self.parent_widget.timer_label.setText(str(self.parent_widget.timer))
        if self.parent_widget.timer <= 0:
            self.parent_widget.mutex.lock()
            self.parent_widget.timer = SECONDS_TO_LEVEL
            self.parent_widget.mutex.unlock()
            self.timer_signal.emit()
        time.sleep(1)


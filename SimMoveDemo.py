import sys
from PyQt5 import QtCore
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QImage, QPalette, QBrush, QFont
from PyQt5.QtWidgets import *
from KeyNotifier import *
from player import Player
import time
from multiprocessing import Process, Queue
from threading import Thread
from MovingCars import CarMoving
from MovingLogs import LogMoving
from MovingTurtles import TurtleMoving
from CollisionNotifier import CollisionNotifier
from Collisions import *
from Menu import *


class SimMoveDemo(QWidget):

    def __init__(self):
        super().__init__()

        self.pix1 = QPixmap("pictures/frog.png")

        self.label1 = QLabel(self)
        self.label2 = QLabel(self)

        self.labelF1 = QLabel(self)
        self.labelF1Obj = FinishObj(self, 15)
        self.labelF2 = QLabel(self)
        self.labelF2Obj = FinishObj(self, 118)
        self.labelF3 = QLabel(self)
        self.labelF3Obj = FinishObj(self, 221)
        self.labelF4 = QLabel(self)
        self.labelF4Obj = FinishObj(self, 323)
        self.labelF5 = QLabel(self)
        self.labelF5Obj = FinishObj(self, 425)

        self.movingCar = CarMoving(self)
        self.movingTurtle = TurtleMoving(self)
        self.movingLog = LogMoving(self)

        self.finishObjs = [self.labelF1Obj, self.labelF2Obj, self.labelF3Obj, self.labelF4Obj, self.labelF5Obj]
        self.scoreLabel = QLabel(self)
        self.scoreCounterLabel = QLabel(self)
        self.livesLabel = QLabel(self)
        self.livesCounter = QLabel(self)
        self.levelLable = QLabel(self)

        self.onTurtle = False
        self.onLog = False

        self.level = 1
        self.check_point = 0

        self.player1 = Player(self.label1)
        self.__init_ui__()

        self.key_notifier = KeyNotifier()
        self.key_notifier.key_signal.connect(self.__frogMovement__)
        self.key_notifier.start()

        self.collision_notifier = CollisionNotifier()
        #self.collision_notifier.collisionSignal.connect(self.__car_collision__)
        #self.collision_notifier.collisionSignal.connect(self.__log_collision__)
        #self.collision_notifier.collisionSignal.connect(self.__turtle_collision__)
        #self.collision_notifier.collisionSignal.connect(self.__in_river)
        self.collision_notifier.start()

    def __init_ui__(self):

        self.setGeometry(500, 300, 480, 600)
        self.setFixedSize(self.size())
        oImage = QImage("pictures/background.png")
        sImage = oImage.scaled(QSize(480, 600))
        palette = QPalette()
        palette.setBrush(10, QBrush(sImage))
        self.setPalette(palette)

        font = QFont()
        font.setBold(True)
        font.setPointSize(16)

        self.pixScore = QPixmap("pictures/score.png")
        self.scoreLabel.setGeometry(20, 20, 100, 20)
        self.scoreLabel.setPixmap(self.pixScore)
        self.scoreCounterLabel.setGeometry(140, 20, 100, 20)
        self.scoreCounterLabel.setText(str(self.player1.score))
        self.scoreCounterLabel.setFont(font)

        self.levelLable.setGeometry(230, 20, 30, 20)
        self.levelLable.setText(str(self.level))
        self.levelLable.setFont(font)

        self.livesPix = QPixmap("pictures/lives.png")
        self.livesLabel.setPixmap(self.livesPix)
        self.livesLabel.setGeometry(300, 20, 100, 21)
        self.livesCounter.setGeometry(420, 20, 100, 20)
        self.livesCounter.setText(str(self.player1.lives))
        self.livesCounter.setFont(font)
        #self.scoreCounterLabel.setStyleSheet("{color: #EA4335}")

        self.label1.setPixmap(self.pix1)
        self.label1.setGeometry(220, 560, 40, 40)
        self.label1.raise_()

        self.setWindowTitle("Frogger")
        self.show()

    def keyPressEvent(self, event):
        self.key_notifier.add_key(event.key())

    def keyReleaseEvent(self, event):
        self.key_notifier.rem_key(event.key())
        if event.key() == Qt.Key_Right and self.player1.isDead is False:
            self.pix1 = QPixmap("pictures/frog_right.png")
        elif event.key() == Qt.Key_Left and self.player1.isDead is False:
            self.pix1 = QPixmap("pictures/frog_left.png")
        elif event.key() == Qt.Key_Up and self.player1.isDead is False:
            self.pix1 = QPixmap("pictures/frog.png")
        elif event.key() == Qt.Key_Down and self.player1.isDead is False:
            self.pix1 = QPixmap("pictures/frog_back.png")
        self.label1.setPixmap(self.pix1)

    def closeEvent(self, event):
        self.key_notifier.die()
        self.collision_notifier.die()
        self.movingCar.close()
        self.movingLog.close()
        self.movingTurtle.close()

    def __car_collision__(self):
        CarCollision.detect(self)

    def __log_collision__(self):
        LogCollision.detect(self)

    def __turtle_collision__(self):
        TurtleCollision.detect(self)

    def __is_frog_in_screen__(self, x, y):
        if (x < -10 or x + 40 > 490 or y < 50 or y > 590):
            return False
        else:
            return True

    def moveFrog(self, x, y):
        self.label1.setGeometry(x, y, 40, 40)
        if self.__is_frog_in_screen__(x, y) is False:
            self.lose_life()
        else:
            self.__check_frog_movement__(x, y)

    def __in_river(self):
        frog = self.label1.geometry()
        if frog.y() < 320 and frog.y() > 80:
            if not self.onTurtle and not self.onLog:
                self.label1.setGeometry(220, 560, 40, 40)

    def level_up(self):
        self.level += 1
        self.levelLable.setText(str(self.level))
        self.movingTurtle.turtleSpeed += 1
        self.movingLog.logSpeed += 1
        self.movingCar.carSpeed += 1
        for obj in self.finishObjs:
            obj.reset()

    def __get_check_point__(self):
        self.check_point += 1
        self.player1.updateScore(200)
        self.scoreCounterLabel.setText(str(self.player1.score))
        self.player1.stepMax = 560
        if self.check_point == 5:
            self.check_point = 0
            self.level_up()

    def __check_frog_movement__(self, x, y):
        if (y > 50 and y < 120):
            if (x>10 and x<21) and self.finishObjs[0].finished is False:
                self.finishObjs[0].finish()
                self.__get_check_point__()
                self.moveFrog(220, 560)
            elif (x>113 and x<123) and self.finishObjs[1].finished is False:
                self.finishObjs[1].finish()
                self.__get_check_point__()
                self.moveFrog(220, 560)
            elif (x>216 and x<226) and self.finishObjs[2].finished is False:
                self.finishObjs[2].finish()
                self.__get_check_point__()
                self.moveFrog(220, 560)
            elif (x>318 and x<328) and self.finishObjs[3].finished is False:
                self.finishObjs[3].finish()
                self.__get_check_point__()
                self.moveFrog(220, 560)
            elif (x>418 and x<430) and self.finishObjs[4].finished is False:
                self.finishObjs[4].finish()
                self.__get_check_point__()
                self.moveFrog(220, 560)
            else:
                self.lose_life()

    def lose_life(self):
        self.moveFrog(220, 560)
        self.player1.stepMax=560
        self.player1.updateLives()
        self.livesCounter.setText(str(self.player1.lives))
        if self.player1.isDead is True:
            self.label1.destroy()
            self.death()

    def death(self):
        self.movingCar.close()
        self.movingLog.close()
        self.movingTurtle.close()

    def __frogMovement__(self, key):
        rec1 = self.label1.geometry()

        if key == Qt.Key_Right and self.player1.isDead is False:
            self.pix1 = QPixmap("pictures/frog_right_jump.png")
            self.label1.setPixmap(self.pix1)
            self.moveFrog(rec1.x() + 25, rec1.y())
        elif key == Qt.Key_Down and self.player1.isDead is False:
            self.pix1 = QPixmap("pictures/frog_back_jump.png")
            self.label1.setPixmap(self.pix1)
            self.moveFrog(rec1.x(), rec1.y() + 40)
        elif key == Qt.Key_Up and self.player1.isDead is False:
            self.pix1 = QPixmap("pictures/frog_jump.png")
            self.label1.setPixmap(self.pix1)
            self.moveFrog(rec1.x(), rec1.y() - 40)
            rec1 = self.label1.geometry()
            if self.player1.stepMax > rec1.y():
                self.player1.stepMax = rec1.y()
                self.player1.updateScore(10)
                self.scoreCounterLabel.setText(str(self.player1.score))
        elif key == Qt.Key_Left and self.player1.isDead is False:
            self.pix1 = QPixmap("pictures/frog_left_jump.png")
            self.label1.setPixmap(self.pix1)
            self.moveFrog(rec1.x() - 25, rec1.y())
        elif key == Qt.Key_Escape:
            sys.exit()


class FinishObj(QWidget):
    def __init__(self, parent, x):
        super().__init__(parent)
        self.frog_safe = QLabel(self)
        self.pix_frog_safe = QPixmap("pictures/frog_safe.png")
        self.frog_safe.setPixmap(self.pix_frog_safe)
        self.frog_safe.setGeometry(x, 80, 40, 40)
        self.hide()
        self.finished = False

    def finish(self):
        self.finished = True
        self.show()

    def reset(self):
        self.finished = False
        self.hide()

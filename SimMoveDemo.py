import sys
from PyQt5 import QtCore
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QImage, QPalette, QBrush, QFont
from PyQt5.QtWidgets import *
from KeyNotifier import *
from player import Player
import time
from multiprocessing import Process, Queue, Pipe
from threading import Thread
from MovingCars import CarMoving
from MovingLogs import LogMoving
from MovingTurtles import TurtleMoving
from CollisionNotifier import CollisionNotifier
from Collisions import *
from PyQt5.QtCore import pyqtSignal, Qt, QMutex
from Menu import *
from FlyBonus import *
from FlyBonusThread import *
import multiprocessing as mp


class SimMoveDemo(QWidget):
    mutex = QMutex()
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
        self.gameOverLabel = QLabel(self)
        self.onTurtle = False
        self.onLog = False

        self.level = 1
        self.check_point = 0

        self.player1 = Player(self.label1, 300)
        self.player2 = Player(self.label2, 140)
        self.players = [self.player1, self.player2]
        self.__init_ui__()

        self.key_notifier = KeyNotifier()
        self.key_notifier.key_signal.connect(self.__frogMovement__)
        self.key_notifier.start()

        self.collision_notifier = CollisionNotifier()
        #self.collision_notifier.collisionSignal.connect(self.__car_collision__)
       # self.collision_notifier.collisionSignal.connect(self.__log_collision__)
        #self.collision_notifier.collisionSignal.connect(self.__turtle_collision__)
      #  self.collision_notifier.collisionSignal.connect(self.__in_river)
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

        self.gameOverLabel.setGeometry(160, 250, 170, 50)
        self.gameOverLabel.setText(str("GAME OVER"))
        self.gameOverLabel.setFont(font)
        self.gameOverLabel.hide()

        self.livesPix = QPixmap("pictures/lives.png")
        self.livesLabel.setPixmap(self.livesPix)
        self.livesLabel.setGeometry(300, 20, 100, 21)
        self.livesCounter.setGeometry(420, 20, 100, 20)
        self.livesCounter.setText(str(self.player1.lives))
        self.livesCounter.setFont(font)
        #self.scoreCounterLabel.setStyleSheet("{color: #EA4335}")

        self.label1.setPixmap(self.pix1)
        self.label1.setGeometry(300, 560, 40, 40)
        self.label1.raise_()

        self.label2.setPixmap(self.pix1)
        self.label2.setGeometry(140, 560, 40, 40)
        self.label2.raise_()

        self.setWindowTitle("Frogger")
        self.show()

        self.ex_pipe, self.in_pipe = Pipe()
        self.flyBonusProcess = FlyBonus(pipe=self.ex_pipe, checkPoints=5)
        self.flyBonusThread = FlyBonusThread(self)
        self.flyBonusProcess.start()
        self.flyBonusThread.start()

    def keyPressEvent(self, event):
        self.key_notifier.add_key(event.key())

    def keyReleaseEvent(self, event):
        self.key_notifier.rem_key(event.key())
        if event.key() == Qt.Key_Right and self.player1.isDead is False:
            self.pix1 = QPixmap("pictures/frog_right.png")
            self.label1.setPixmap(self.pix1)
        elif event.key() == Qt.Key_Left and self.player1.isDead is False:
            self.pix1 = QPixmap("pictures/frog_left.png")
            self.label1.setPixmap(self.pix1)
        elif event.key() == Qt.Key_Up and self.player1.isDead is False:
            self.pix1 = QPixmap("pictures/frog.png")
            self.label1.setPixmap(self.pix1)
        elif event.key() == Qt.Key_Down and self.player1.isDead is False:
            self.pix1 = QPixmap("pictures/frog_back.png")
            self.label1.setPixmap(self.pix1)
        elif event.key() == Qt.Key_D and self.player2.isDead is False:
            self.pix1 = QPixmap("pictures/frog_right.png")
            self.label2.setPixmap(self.pix1)
        elif event.key() == Qt.Key_A and self.player2.isDead is False:
            self.pix1 = QPixmap("pictures/frog_left.png")
            self.label2.setPixmap(self.pix1)
        elif event.key() == Qt.Key_W and self.player2.isDead is False:
            self.pix1 = QPixmap("pictures/frog.png")
            self.label2.setPixmap(self.pix1)
        elif event.key() == Qt.Key_S and self.player2.isDead is False:
            self.pix1 = QPixmap("pictures/frog_back.png")
            self.label2.setPixmap(self.pix1)


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

    def moveFrog(self, x, y,player):
        player.label.setGeometry(x, y, 40, 40)
        if self.__is_frog_in_screen__(x, y) is False:
            self.lose_life(player)
        else:
            self.__check_frog_movement__(x, y, player)

    def __in_river(self):
        for player in self.players:
            frog = player.label.geometry()
            if frog.y() < 320 and frog.y() > 80:
                if not player.onTurtle and not player.onLog:
                    #player.label.setGeometry(220, 560, 40, 40)
                    self.lose_life(self.player1)
                    self.lose_life(self.player2)

    def level_up(self):
        self.level += 1
        self.levelLable.setText(str(self.level))
        self.movingTurtle.speed_up()
        self.movingLog.speed_up()
        self.movingCar.speed_up()
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

    def __check_frog_movement__(self, x, y, player):
        if (y > 50 and y < 120):
            if (x>10 and x<21) and self.finishObjs[0].finished is False:
                if self.finishObjs[0].hasFlyBonus is True:
                    self.player1.updateScore(400)
                    self.scoreCounterLabel.setText(str(self.player1.score))
                    self.finishObjs[0].hideBonus()
                self.finishObjs[0].finish()
                self.__get_check_point__()
                self.moveFrog(player.start, 560, player)
            elif (x>113 and x<123) and self.finishObjs[1].finished is False:
                if self.finishObjs[1].hasFlyBonus is True:
                    self.player1.updateScore(400)
                    self.scoreCounterLabel.setText(str(self.player1.score))
                    self.finishObjs[1].hideBonus()
                self.finishObjs[1].finish()
                self.__get_check_point__()
                self.moveFrog(player.start, 560, player)
            elif (x>216 and x<226) and self.finishObjs[2].finished is False:
                if self.finishObjs[2].hasFlyBonus is True:
                    self.player1.updateScore(400)
                    self.scoreCounterLabel.setText(str(self.player1.score))
                    self.finishObjs[2].hideBonus()
                self.finishObjs[2].finish()
                self.__get_check_point__()
                self.moveFrog(player.start, 560, player)
            elif (x>318 and x<328) and self.finishObjs[3].finished is False:
                if self.finishObjs[3].hasFlyBonus is True:
                    self.player1.updateScore(400)
                    self.scoreCounterLabel.setText(str(self.player1.score))
                    self.finishObjs[3].hideBonus()
                print("cetvrti ulaz")
                self.finishObjs[3].finish()
                self.__get_check_point__()
                self.moveFrog(player.start, 560, player)
            elif (x>418 and x<430) and self.finishObjs[4].finished is False:
                if self.finishObjs[4].hasFlyBonus is True:
                    self.player1.updateScore(400)
                    self.scoreCounterLabel.setText(str(self.player1.score))
                    self.finishObjs[4].hideBonus()
                self.finishObjs[4].finish()
                self.__get_check_point__()
                self.moveFrog(player.start, 560, player)
            else:
                self.lose_life(self.player1)
                self.lose_life(self.player2)

    def death(self):
        self.movingCar.close()
        self.movingLog.close()
        self.movingTurtle.close()
        self.gameOverLabel.show()

    def lose_life(self, player):
        self.moveFrog(player.start, 560, player)
        player.stepMax = 560
        player.updateLives()
        self.livesCounter.setText(str(player.lives))
        if player.isDead is True:
            player.label.destroy()
            self.death()

    def __frogMovement__(self, key):
        rec1 = self.label1.geometry()
        rec2 = self.label2.geometry()

        if key == Qt.Key_Right and self.player1.isDead is False:
            self.pix1 = QPixmap("pictures/frog_right_jump.png")
            self.label1.setPixmap(self.pix1)
            self.moveFrog(rec1.x() + 25, rec1.y(), self.player1)
        elif key == Qt.Key_Down and self.player1.isDead is False:
            self.pix1 = QPixmap("pictures/frog_back_jump.png")
            self.label1.setPixmap(self.pix1)
            self.moveFrog(rec1.x(), rec1.y() + 40, self.player1)
        elif key == Qt.Key_Up and self.player1.isDead is False:
            self.pix1 = QPixmap("pictures/frog_jump.png")
            self.label1.setPixmap(self.pix1)
            self.moveFrog(rec1.x(), rec1.y() - 40,self.player1)
            rec1 = self.player1.label.geometry()
            if self.player1.stepMax > rec1.y():
                self.player1.stepMax = rec1.y()
                self.player1.updateScore(10)
                self.scoreCounterLabel.setText(str(self.player1.score))
        elif key == Qt.Key_Left and self.player1.isDead is False:
            self.pix1 = QPixmap("pictures/frog_left_jump.png")
            self.label1.setPixmap(self.pix1)
            self.moveFrog(rec1.x() - 25, rec1.y(), self.player1)
        elif key == Qt.Key_Escape:
            sys.exit()
        elif key == Qt.Key_D and self.player2.isDead is False:
            self.pix1 = QPixmap("pictures/frog_right_jump.png")
            self.label2.setPixmap(self.pix1)
            self.moveFrog(rec2.x() + 25, rec2.y(), self.player2)
        elif key == Qt.Key_S and self.player2.isDead is False:
            self.pix1 = QPixmap("pictures/frog_back_jump.png")
            self.label2.setPixmap(self.pix1)
            self.moveFrog(rec2.x(), rec2.y() + 40, self.player2)
        elif key == Qt.Key_W and self.player2.isDead is False:
            self.pix1 = QPixmap("pictures/frog_jump.png")
            self.label2.setPixmap(self.pix1)
            self.moveFrog(rec2.x(), rec2.y() - 40, self.player2)
            rec2 = self.label2.geometry()
            if self.player2.stepMax > rec2.y():
                self.player2.stepMax = rec2.y()
                self.player1.updateScore(10)
                self.scoreCounterLabel.setText(str(self.player1.score))
        elif key == Qt.Key_A and self.player2.isDead is False:
            self.pix1 = QPixmap("pictures/frog_left_jump.png")
            self.label2.setPixmap(self.pix1)
            self.moveFrog(rec2.x() - 25, rec2.y(), self.player2)


class FinishObj(QWidget):
    def __init__(self, parent, x):
        super().__init__(parent)
        self.frog_safe = QLabel(self)
        self.pix_frog_safe = QPixmap("pictures/frog_safe.png")
        self.pix_fly_bonus = QPixmap("pictures/fly.png")
        self.frog_safe.setGeometry(x, 80, 40, 40)
        self.hasFlyBonus = False
        self.hide()
        self.finished = False

    def finish(self):
        self.finished = True
        self.frog_safe.setPixmap(self.pix_frog_safe)
        self.show()


    def reset(self):
        self.finished = False
        self.hide()

    def showBonus(self):
        self.frog_safe.setPixmap(self.pix_fly_bonus)
        self.show()
        self.hasFlyBonus = True

    def hideBonus(self):
        self.hide()
        self.hasFlyBonus = False
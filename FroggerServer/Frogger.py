import sys
from PyQt5 import QtCore
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QImage, QPalette, QBrush, QFont
from PyQt5.QtWidgets import *
from GamePlay import *
import time
from multiprocessing import Process, Queue, Pipe
from threading import Thread
from MovingCars import CarMoving
from MovingLogs import LogMoving
from MovingTurtles import TurtleMoving
from CollisionNotifier import CollisionNotifier
from Collisions import *
from PyQt5.QtCore import pyqtSignal, Qt, QMutex
from Server import *
import multiprocessing as mp
from Threads import *
import pickle
from FlyBonusThread import *
from Enums import GameMode


class SimMoveDemo(QWidget):
    mutex = QMutex()

    def __init__(self, connection, mode, connection2=None):
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
        self.scoreLabel2 = QLabel(self)
        self.scoreCounterLabel2 = QLabel(self)
        self.livesLabel2 = QLabel(self)
        self.livesCounter2 = QLabel(self)
        self.levelLable = QLabel(self)
        self.gameOverLabel = QLabel(self)
        self.winner = QLabel(self)
        self.timer_label = QLabel(self)
        self.level_up_label = QLabel(self)
        self.timer = 30
        self.winner_text = ''

        self.onTurtle = False
        self.onLog = False

        self.level = 1
        self.check_point = 0
        self.game_over = False
        self.game_over_result = 0
        self.game_mode = mode

        self.player1 = Player(self.label1, 140, self.scoreCounterLabel, self.livesCounter, connection)
        self.start_game = "NEW"
        connection.sendall(self.start_game.encode('utf8'))
        if connection2 is None:
            self.player2 = Player(self.label2, 300, self.scoreCounterLabel2, self.livesCounter2, connection)
        else:
            time.sleep(1)
            self.player2 = Player(self.label2, 300, self.scoreCounterLabel2, self.livesCounter2, connection2)
            connection2.sendall(self.start_game.encode('utf8'))

        self.players = [self.player1, self.player2]
        self.__init_ui__()

        self.receive = ''
        self.send = ''

        self.collision_notifier = CollisionNotifier()
        self.collision_notifier.collisionSignal.connect(self.__car_collision__)
        self.collision_notifier.collisionSignal.connect(self.__log_collision__)
        self.collision_notifier.collisionSignal.connect(self.__turtle_collision__)
        self.collision_notifier.collisionSignal.connect(self.__in_river)
        self.collision_notifier.start()

        self.timer_thread = TimerClass(self)
        self.timer_thread.timer_signal.connect(self.level_up)
        self.timer_thread.start()

        self.conn = connection
        self.conn2 = connection2
        self.winner_conn = 0
        self.new_game = True

        self.text = ''
        self.result_string1 = ''
        self.result_string2 = ''
        self.result_string0 = ''

        self.__communication_threads__()

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
        self.scoreLabel.setGeometry(10, 10, 80, 20)
        self.scoreLabel.setPixmap(self.pixScore)
        self.scoreLabel2.setGeometry(310, 10, 80, 20)
        self.scoreLabel2.setPixmap(self.pixScore)

        self.scoreCounterLabel.setGeometry(100, 10, 80, 20)
        self.scoreCounterLabel.setText(str(0))
        self.scoreCounterLabel.setFont(font)
        self.scoreCounterLabel2.setGeometry(400, 10, 80, 20)
        self.scoreCounterLabel2.setText(str(0))
        self.scoreCounterLabel2.setFont(font)

        self.timer_label.setGeometry(210, 10, 50, 20)
        self.timer_label.setText(str(self.timer))
        self.timer_label.setFont(font)

        self.levelLable.setGeometry(210, 30, 30, 20)
        self.levelLable.setText(str(self.level))
        self.levelLable.setFont(font)

        self.gameOverLabel.setGeometry(160, 200, 170, 50)
        self.gameOverLabel.setText(str("GAME OVER"))
        self.gameOverLabel.setFont(font)
        self.gameOverLabel.hide()

        self.winner.setGeometry(80, 250, 350, 50)
        self.winner.setFont(font)
        self.winner.hide()

        self.livesPix = QPixmap("pictures/lives.png")
        self.livesLabel.setPixmap(self.livesPix)
        self.livesLabel.setGeometry(10, 30, 80, 20)
        self.livesCounter.setGeometry(100, 30, 80, 20)
        self.livesCounter.setText(str(3))
        self.livesCounter.setFont(font)

        self.livesLabel2.setPixmap(self.livesPix)
        self.livesLabel2.setGeometry(310, 30, 80, 20)
        self.livesCounter2.setGeometry(400, 30, 80, 20)
        self.livesCounter2.setText(str(3))
        self.livesCounter2.setFont(font)

        self.label1.setPixmap(self.pix1)
        self.label1.setGeometry(140, 560, 40, 40)
        self.label1.raise_()

        self.label2.setPixmap(self.pix1)
        self.label2.setGeometry(300, 560, 40, 40)
        self.label2.raise_()

        self.setWindowTitle("Frogger")
        self.show()

        self.ex_pipe, self.in_pipe = Pipe()
        self.flyBonusProcess = FlyBonus(pipe=self.ex_pipe, checkPoints=5)
        self.flyBonusThread = FlyBonusThread(self)
        self.flyBonusProcess.start()
        self.flyBonusThread.start()

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
                    self.lose_life(player)

    def level_up(self):
        self.level += 1
        self.levelLable.setText(str(self.level))
        self.moveFrog(self.player1.start, 560, self.player1)
        self.moveFrog(self.player2.start, 560, self.player2)
        self.movingTurtle.speed_up()
        self.movingLog.speed_up()
        self.movingCar.speed_up()

    def __get_check_point__(self, player):
        self.check_point += 1
        player.updateScore(200)
        player.stepMax = 560
        if self.check_point == 5:
            self.death()

    def __check_frog_movement__(self, x, y, player):
        if (y > 50 and y < 120):
            if (x>10 and x<21) and self.finishObjs[0].finished is False:
                if self.finishObjs[0].hasFlyBonus is True:
                    player.updateScore(400)
                    self.finishObjs[0].hideBonus()
                self.finishObjs[0].finish()
                self.__get_check_point__(player)
                self.moveFrog(player.start, 560, player)
            elif (x>113 and x<123) and self.finishObjs[1].finished is False:
                if self.finishObjs[1].hasFlyBonus is True:
                    player.updateScore(400)
                    self.finishObjs[1].hideBonus()
                self.finishObjs[1].finish()
                self.__get_check_point__(player)
                self.moveFrog(player.start, 560, player)
            elif (x>216 and x<226) and self.finishObjs[2].finished is False:
                if self.finishObjs[2].hasFlyBonus is True:
                    player.updateScore(400)
                    self.finishObjs[2].hideBonus()
                self.finishObjs[2].finish()
                self.__get_check_point__(player)
                self.moveFrog(player.start, 560, player)
            elif (x>318 and x<328) and self.finishObjs[3].finished is False:
                if self.finishObjs[3].hasFlyBonus is True:
                    player.updateScore(400)
                    self.finishObjs[3].hideBonus()
                self.finishObjs[3].finish()
                self.__get_check_point__(player)
                self.moveFrog(player.start, 560, player)
            elif (x>418 and x<430) and self.finishObjs[4].finished is False:
                if self.finishObjs[4].hasFlyBonus is True:
                    player.updateScore(400)
                    self.finishObjs[4].hideBonus()
                self.finishObjs[4].finish()
                self.__get_check_point__(player)
                self.moveFrog(player.start, 560, player)
            else:
                self.lose_life(player)

    def death(self):
        self.game_end()
        self.movingCar.close()
        self.movingLog.close()
        self.movingTurtle.close()
        self.collision_notifier.die()
        time.sleep(1)
        self.send.was_cancelled = True
        self.receive.die()
        if self.conn2 is not None:
            self.send2.was_cancelled = True
            self.receive2.die()
        self.flyBonusThread.die()
        self.flyBonusProcess.die()
        self.timer_thread.die()
        self.close()

    def game_end(self):
        self.gameOverLabel.show()
        if self.game_mode == GameMode.MULTYPLAYER_OFFLINE:       
            if self.players[0].score > self.players[1].score:
                self.winner_conn = self.conn
                self.text = 'WL_'
                self.result_string0 = 'WL'
            else:
                self.text = 'LW_'
                self.result_string0 = 'LW'
                self.winner_conn = self.conn2
        elif self.game_mode == GameMode.MULTYPLAYER_ONLINE:
            if self.players[0].score > self.players[1].score:
                self.result_string1 = 'WINNER'
                self.result_string2 = 'LOSER'
                self.winner_conn = self.conn
            else:
                self.result_string2 = 'WINNER'
                self.result_string1 = 'LOSER'
                self.winner_conn = self.conn2
        elif self.game_mode == GameMode.TOURNAMENT:
            if self.players[0].score > self.players[1].score:
                self.winner_conn = self.conn
                self.result_string1 = 'NEXT'
                self.result_string2 = 'LOSER'
            else:
                self.result_string2 = 'NEXT'
                self.result_string1 = 'LOSER'
                self.winner_conn = self.conn2
        elif self.game_mode == GameMode.FINALE:
            if self.players[0].score > self.players[1].score:
                self.winner_conn = self.conn
                self.result_string1 = 'TWINNER'
                self.result_string2 = 'LOSER'
            else:
                self.result_string2 = 'TWINNER'
                self.result_string1 = 'LOSER'
                self.winner_conn = self.conn2
        self.game_over = True
        self.winner.setText(self.winner_text)
        self.winner.show()

    def lose_life(self, player):
        self.moveFrog(player.start, 560, player)
        player.stepMax = 560
        player.updateLives()
        if self.players[0].isDead is True and self.players[1].isDead is True:
            if self.players[0].score == self.players[1].score:
                self.players[0].bonus_life()
                self.players[1].bonus_life()
            else:
                self.game_over = True
                self.players[0].die()
                self.players[1].die()
                self.death()

    def __frogMovement__(self, key):
        rec1 = self.label1.geometry()
        rec2 = self.label2.geometry()

        if key == Qt.Key_Right and self.player2.isDead is False:
            self.moveFrog(rec2.x() + 25, rec2.y(), self.player2)
        elif key == Qt.Key_Down and self.player2.isDead is False:
            self.moveFrog(rec2.x(), rec2.y() + 40, self.player2)
        elif key == Qt.Key_Up and self.player2.isDead is False:
            self.moveFrog(rec2.x(), rec2.y() - 40,self.player2)
            rec2 = self.player2.label.geometry()
            if self.player2.stepMax > rec2.y():
                self.player2.stepMax = rec2.y()
                self.player2.updateScore(10)
        elif key == Qt.Key_Left and self.player2.isDead is False:
            self.moveFrog(rec2.x() - 25, rec2.y(), self.player2)
        elif key == Qt.Key_Escape:
            sys.exit()
        elif key == Qt.Key_D and self.player1.isDead is False:
            self.moveFrog(rec1.x() + 25, rec1.y(), self.player1)
        elif key == Qt.Key_S and self.player1.isDead is False:
            self.moveFrog(rec1.x(), rec1.y() + 40, self.player1)
        elif key == Qt.Key_W and self.player1.isDead is False:
            self.moveFrog(rec1.x(), rec1.y() - 40, self.player1)
            rec1 = self.label1.geometry()
            if self.player1.stepMax > rec1.y():
                self.player1.stepMax = rec1.y()
                self.player1.updateScore(10)
        elif key == Qt.Key_A and self.player1.isDead is False:
            self.moveFrog(rec1.x() - 25, rec1.y(), self.player1)

    def __communication_threads__(self):
        if self.conn is not None and self.conn2 is not None:
            self.receive = Receive(self.conn, 1)
            self.receive.key_signal.connect(self.__frogMovement__)
            self.send = Send(self.conn,1, self)
            self.receive.start()
            self.send.start()
            self.receive2 = Receive(self.conn2, 2)
            self.receive2.key_signal.connect(self.__frogMovement__)
            self.send2 = Send(self.conn2, 2, self)
            self.receive2.start()
            self.send2.start()
        elif self.conn is not None:
            self.receive = Receive(self.conn, 0)
            self.receive.key_signal.connect(self.__frogMovement__)
            self.send = Send(self.conn, 0, self)
            self.receive.start()
            self.send.start()
        self.new_game = False


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

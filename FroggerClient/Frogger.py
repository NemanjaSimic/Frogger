# Echo client program
import pickle
import sys
from PyQt5 import QtCore
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QImage, QPalette, QBrush, QFont
from PyQt5.QtWidgets import *
from  Labels import *
from Threads import *

HOST = 'localhost'  # The remote host
PORT = 50006        # The same port as used by the server


class Gui(QWidget):
    def __init__(self, mode, IP):
        super().__init__()
        self.host = IP
        self.pix1 = QPixmap("pictures/frog.png")
        self.pix_frog_safe = QPixmap("pictures/frog_safe.png")
        self.pix_fly_bonus = QPixmap("pictures/fly.png")
        self.pix_score = QPixmap("pictures/score.png")
        self.pix_lives = QPixmap("pictures/lives.png")

        self.frog_safe1 = QLabel(self)
        self.frog_safe2 = QLabel(self)
        self.frog_safe3 = QLabel(self)
        self.frog_safe4 = QLabel(self)
        self.frog_safe5 = QLabel(self)

        self.label1 = QLabel(self)
        self.label2 = QLabel(self)

        self.labelF1 = QLabel(self)
        self.labelF2 = QLabel(self)
        self.labelF3 = QLabel(self)
        self.labelF4 = QLabel(self)
        self.labelF5 = QLabel(self)

        self.scoreLabel = QLabel(self)
        self.scoreCounterLabel = QLabel(self)
        self.livesLabel = QLabel(self)
        self.livesCounter = QLabel(self)
        self.levelLable = QLabel(self)
        self.scoreLabel2 = QLabel(self)
        self.scoreCounterLabel2 = QLabel(self)
        self.livesLabel2 = QLabel(self)
        self.livesCounter2 = QLabel(self)
        self.gameOverLabel = QLabel(self)
        self.winner = QLabel(self)
        self.timer_label = QLabel(self)
        self.next_round_label = QLabel(self)
        self.winner_of_tour_label = QLabel(self)
        self.lost_label = QLabel(self)
        self.lw_label = QLabel(self)
        self.wl_label = QLabel(self)
        #self.exitBtn = QPushButton('MENU', self)

        self.movingCars = ''
        self.movingTurtles = ''
        self.movingLogs = ''

        self.receive = QThread()
        self.connected = False
        self.tournament = 0
        self.send = ''
        self.mode = mode
        self.s = ''

        self.__init_ui__()
        self.connectThreads()

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

        self.scoreLabel.setGeometry(10, 10, 80, 20)
        self.scoreLabel.setPixmap(self.pix_score)
        self.scoreLabel2.setGeometry(310, 10, 80, 20)
        self.scoreLabel2.setPixmap(self.pix_score)

        self.scoreCounterLabel.setGeometry(100, 10, 80, 20)
        self.scoreCounterLabel2.setGeometry(400, 10, 80, 20)
        self.scoreCounterLabel.setFont(font)
        self.scoreCounterLabel2.setFont(font)

        self.levelLable.setGeometry(210, 30, 30, 20)
        self.levelLable.setText(str(1))
        self.levelLable.setFont(font)

        self.gameOverLabel.setGeometry(160, 200, 170, 50)
        self.gameOverLabel.setText(str("GAME OVER"))
        self.gameOverLabel.setFont(font)
        self.gameOverLabel.hide()

        self.lw_label.setGeometry(80, 200, 350, 50)
        self.lw_label.setText(str("RIGHT PLAYER WON !"))
        self.lw_label.setFont(font)
        self.lw_label.hide()

        self.wl_label.setGeometry(80, 200, 350, 50)
        self.wl_label.setText(str("RIGHT PLAYER WON !"))
        self.wl_label.setFont(font)
        self.wl_label.hide()

        self.winner.setGeometry(160, 200, 350, 50)
        self.winner.setText(str("YOU WON !"))
        self.winner.setFont(font)
        self.winner.hide()

        self.lost_label.setGeometry(160, 200, 170, 50)
        self.lost_label.setText(str("YOU LOST !"))
        self.lost_label.setFont(font)
        self.lost_label.hide()

        self.next_round_label.setGeometry(60, 200, 350, 50)
        self.next_round_label.setText(str("WAITING FOR NEXT ROUND..."))
        self.next_round_label.setFont(font)
        self.next_round_label.hide()
        
        self.winner_of_tour_label.setGeometry(80, 200, 350, 50)
        self.winner_of_tour_label.setText(str("YOU WON TOURNAMENT !!!"))
        self.winner_of_tour_label.setFont(font)
        self.winner_of_tour_label.hide()

        self.timer_label.setGeometry(210, 10, 50, 20)
        self.timer_label.setText(str(30))
        self.timer_label.setFont(font)

        self.livesLabel.setPixmap(self.pix_lives)
        self.livesLabel.setGeometry(10, 30, 80, 20)
        self.livesCounter.setGeometry(100, 30, 80, 20)
        self.livesCounter.setFont(font)

        self.livesLabel2.setPixmap(self.pix_lives)
        self.livesLabel2.setGeometry(310, 30, 80, 20)
        self.livesCounter2.setGeometry(400, 30, 80, 20)
        self.livesCounter2.setFont(font)

        self.label1.setPixmap(self.pix1)
        self.label1.setGeometry(300, 560, 40, 40)
        self.label1.raise_()

        self.label2.setPixmap(self.pix1)
        self.label2.setGeometry(140, 560, 40, 40)
        self.label2.raise_()

        self.frog_safe1.setGeometry(15, 80, 40, 40)
        self.frog_safe1.hide()
        self.frog_safe2.setGeometry(118, 80, 40, 40)
        self.frog_safe2.hide()
        self.frog_safe3.setGeometry(221, 80, 40, 40)
        self.frog_safe3.hide()
        self.frog_safe4.setGeometry(323, 80, 40, 40)
        self.frog_safe4.hide()
        self.frog_safe5.setGeometry(425, 80, 40, 40)
        self.frog_safe5.hide()

        self.check_points = [self.frog_safe1, self.frog_safe2, self.frog_safe3, self.frog_safe4, self.frog_safe5]

        self.show()

    def death(self):
        self.movingCars.close()
        self.movingTurtles.close()
        self.movingLogs.close()
        #self.winner.show()
        #self.gameOverLabel.show()

    def __to_menu__(self):
        exitBtn = QPushButton('MENU', self)
        exitBtn.setGeometry(160, 300, 140, 40)
        exitBtn.clicked.connect(self.__die__)
        exitBtn.show()

    def __die__(self):
        self.send.die()
        self.receive.die()
        self.close()

    def new_game(self):
        self.movingCars = CarMoving(self)
        self.movingTurtles = TurtleMoving(self)
        self.movingLogs = LogMoving(self)
        self.gameOverLabel.hide()
        self.winner.hide()
        self.label1.raise_()
        self.label2.raise_()
        self.next_round_label.hide()
        self.winner_of_tour_label.hide()

    def __movement__(self, frog1, frog2, cars, turtles, logs, level, scores, lives, check_point, timer, turtle_pics):
        self.label1.setGeometry(frog1[0], frog1[1], 40, 40)
        self.label2.setGeometry(frog2[0], frog2[1], 40, 40)
        car_counter = 0
        for v in self.movingCars.vehicles:
            temp_geo = v.geometry()
            v.setGeometry(cars[car_counter], v.y(), v.width(), v.height())
            car_counter += 1

        turtle_counter = 0
        for t in self.movingTurtles.turtles:
            temp_geo = t.geometry()
            t.setGeometry(turtles[turtle_counter], t.y(), t.width(), t.height())
            turtle_counter += 1

        self.movingTurtles.labelTurtle3.setPixmap(self.movingTurtles.turtlesPictures3[turtle_pics[0] - 1])
        self.movingTurtles.label2Turtle3.setPixmap(self.movingTurtles.turtlesPictures2[turtle_pics[1] - 1])

        log_counter = 0
        for l in self.movingLogs.logs:
            l.setGeometry(logs[log_counter], l.y(), l.width(), l.height())
            log_counter += 1

        self.levelLable.setText(str(level))
        self.livesCounter.setText(str(lives[0]))
        self.scoreCounterLabel.setText(str(scores[0]))
        self.livesCounter2.setText(str(lives[1]))
        self.scoreCounterLabel2.setText(str(scores[1]))

        for i in range(0,5):
            if check_point[i] == 2:
                self.check_points[i].setPixmap(self.pix_fly_bonus)
                self.check_points[i].show()
            elif check_point[i] == 1:
                self.check_points[i].setPixmap(self.pix_frog_safe)
                self.check_points[i].show()
            else:
                self.check_points[i].hide()
        
        self.timer_label.setText(str(timer))

    def connectThreads(self):
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.connect((self.host, PORT))
        except Exception as e:
            print("Konekcija pukla:", e)
        print("Connected")
        signal = 'o'
        if self.mode == 1:
            signal = 'b'
        elif self.mode == 2:
            signal = 't'

        self.s.sendall(signal.encode('utf8'))
        self.receive = Receive(self.s, self)
        self.receive.position_signal.connect(self.__movement__)
        self.receive.new_game_signal.connect(self.new_game)
        self.receive.lw_signal.connect(self.__lw__)
        self.receive.wl_signal.connect(self.__wl__)
        self.receive.lose_signal.connect(self.__lose__)
        self.receive.win_signal.connect(self.__win__)
        self.receive.next_signal.connect(self.__next__)
        self.receive.winner_signal.connect(self.__t_winner__)
        self.send = Send(self.s)
        self.receive.start()
        self.send.start()
        self.connected = True

    def keyPressEvent(self, event):
        if self.connected is True:
            self.send.add_key(event.key())

    def __lw__(self):
        self.death()
        self.lw_label.show()
        self.__to_menu__()

    def __wl__(self):
        self.death()
        self.wl_label.show()
        self.__to_menu__()

    def __lose__(self):
        self.death()
        self.lost_label.show()
        self.__to_menu__()

    def __win__ (self):
        self.death()
        self.winner.show()
        self.__to_menu__()

    def __next__(self):
        self.death()
        self.next_round_label.show()

    def __t_winner__(self):
        self.death()
        self.winner_of_tour_label.show()
        self.__to_menu__()

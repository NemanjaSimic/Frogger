from PyQt5 import QtCore
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QImage, QPalette, QBrush, QFont
from PyQt5.QtWidgets import *
from Frogger import *
import sys


class Menu(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(500, 300, 480, 600)
        self.setFixedSize(self.size())
        oImage = QImage("pictures/menu.png")
        sImage = oImage.scaled(QSize(480, 600))
        palette = QPalette()
        palette.setBrush(10, QBrush(sImage))
        self.setPalette(palette)
        self.textBox = QLineEdit(self)
        self.__init_ui__()

    def __init_ui__(self):
        self.setWindowTitle("Frogger")



        playBtn = QPushButton('OFFLINE BATTLE', self)
        playBtn.setGeometry(150, 200, 180, 21)
        playBtn.clicked.connect(self.play)

        battleBtn = QPushButton('ONLINE BATTLE', self)
        battleBtn.setGeometry(150, 300, 180, 21)
        battleBtn.clicked.connect(self.battle)

        tournamentBtn = QPushButton('PLAY TOURNAMENT', self)
        tournamentBtn.setGeometry(150, 400, 180, 21)
        tournamentBtn.clicked.connect(self.tournament)

        exitBtn = QPushButton('EXIT GAME', self)
        exitBtn.setGeometry(150, 500, 180, 21)
        exitBtn.clicked.connect(self.exit)
        
        self.textBox.move(20,20)
        self.textBox.resize(150,40)

        self.show()

    def play(self):
        Gui(0, self.textBox.text())

    def battle(self):
        Gui(1, self.textBox.text())

    def tournament(self):
        Gui(2, self.textBox.text())

    def exit(self):
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Menu()

    sys.exit(app.exec_())

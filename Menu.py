from SimMoveDemo import *
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
        self.game = 0
        self.__init_ui__()

    def __init_ui__(self):
        self.setWindowTitle("Frogger")

        playBtn = QPushButton('START GAME', self)
        playBtn.setGeometry(150, 200, 180, 21)
        playBtn.clicked.connect(self.play)

        tournamentBtn = QPushButton('PLAY TOURNAMENT', self)
        tournamentBtn.setGeometry(150, 300, 180, 21)
        # tournamentBtn.clicked.connect(self.tournament)

        exitBtn = QPushButton('EXIT GAME', self)
        exitBtn.setGeometry(150, 400, 180, 21)
        exitBtn.clicked.connect(self.exit)

        self.show()

    def play(self):
        self.game = SimMoveDemo()
        self.close()

    def exit(self):
        sys.exit()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Menu()
    sys.exit(app.exec_())


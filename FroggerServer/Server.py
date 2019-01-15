from Frogger import *
from PyQt5.QtGui import QImage, QPalette, QBrush
from PyQt5.QtCore import QSize
import multiprocessing as mp
import threading
import sys
from Threads import *
from Enums import GameMode


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
        self.__init_ui__()

        self.queue = []
        self.tournament = []
        self.connections = []

        self.communication = CommunicationThreads(self)
        self.communication.connect_signal.connect(self.start_game)
        self.communication.start()

    def __init_ui__(self):
        self.setWindowTitle("Frogger")

        self.show()

    def start_game(self):
        conn = self.communication.get_last_conn()
        bin = ''
        try:
            bin = conn.recv(1024)
        except Exception as e:
            print("Error", e)
        signal = str(bin, 'utf8')
        if signal == 'o':
            SimMoveDemo(conn, GameMode.MULTYPLAYER_OFFLINE)
        elif signal == 'b':
            if self.queue.__len__() > 0:
                conn2 = self.queue.pop(0)
                try:
                    SimMoveDemo(conn, GameMode.MULTYPLAYER_ONLINE, conn2)
                except Exception as e:
                    print("Error:", e)
            else:
                self.queue.append(conn)
        elif signal == 't':
            if self.tournament.__len__() < 4:
                self.tournament.append(conn)
            if self.tournament.__len__() > 3:
                conn2 = self.tournament.pop(0)
                conn3 = self.tournament.pop(0)
                conn4 = self.tournament.pop(0)
                match1 = SimMoveDemo(conn, GameMode.TOURNAMENT, conn2)
                match2 = SimMoveDemo(conn3, GameMode.TOURNAMENT, conn4)
                th = EndOfGame(match1,match2)
                th.finale_signal.connect(lambda: self.finale(th.winner1, th.winner2))
                th.start()

    def finale(self, player1, player2):
        SimMoveDemo(player1, GameMode.FINALE, player2)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Menu()

    sys.exit(app.exec_())


class EndOfGame(QObject):

    finale_signal = pyqtSignal()

    def __init__(self, game1, game2):
        super().__init__()

        self.game1 = game1
        self.game2 = game2
        self.is_done = False
        self.winner1 = ''
        self.winner2 = ''
        self.finale = []

        self.thread = QThread()
        # move the Worker object to the Thread object
        # "push" self from the current thread to this thread
        self.moveToThread(self.thread)
        # Connect Thread started signal to Worker operational slot method
        self.thread.started.connect(self.__work__)

    def start(self):
        """
        Start notifications.
        """
        self.thread.start()

    def add_key(self, key):
        self.keys.append(key)

    def rem_key(self, key):
        self.keys.remove(key)

    def die(self):
        """
        End notifications.
        """
        self.is_done = True
        self.thread.quit()

    @pyqtSlot()
    def __work__(self):
            while not self.is_done:
                if self.game1.game_over is True:
                    self.winner1 = self.game1.winner_conn
                if self.game2.game_over is True:
                    self.winner2 = self.game2.winner_conn
                if self.game1.game_over is True and self.game2.game_over is True:
                    self.finale_signal.emit()
                    time.sleep(1)
                    self.is_done = True
                time.sleep(1)

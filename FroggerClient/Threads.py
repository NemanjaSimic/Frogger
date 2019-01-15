from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot, Qt, QMutex
import socket
import time
import pickle

HOST = 'localhost'  # The remote host
PORT = 50006        # The same port as used by the server


class KeyNotifier(QObject):

    key_signal = pyqtSignal(int, int)

    def __init__(self):
        super().__init__()

        self.keys = []
        self.is_done = False

        self.thread = QThread()
        # move the Worker object to the Thread object
        # "push" self from the current thread to this thread
        self.moveToThread(self.thread)
        # Connect Thread started signal to Worker operational slot method
        self.thread.started.connect(self.__connection__)

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
        """
        A slot with no params.
        """
        while not self.is_done:
            for k in self.keys:
                self.key_signal.emit(k)
            time.sleep(0.1)

    @pyqtSlot()
    def __connection__(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            print('Connected')
            while not self.is_done:
                #text2send = 'Hello world š đ č ć ž Здраво Свете'
                #s.sendall(text2send.encode('utf8'))
                text = ''
                bin = s.recv(1024)
                x, y = pickle.loads(bin)
                self.key_signal.emit(x, y)
                #text += str(bin, 'utf-8')
                print('Received', text)
                if text == 'r':
                    self.key_signal.emit(Qt.Key_Right)
                elif text == 'l':
                    self.key_signal.emit(Qt.Key_Left)
                elif text == 'd':
                    self.key_signal.emit(Qt.Key_Down)
                elif text == 'u':
                    self.key_signal.emit(Qt.Key_Up)
                time.sleep(0.01)


class Receive(QThread):

    position_signal = pyqtSignal(list, list, list, list, list, int, list, list, list, int, list)
    new_game_signal = pyqtSignal()
    lw_signal = pyqtSignal()
    wl_signal = pyqtSignal()
    lose_signal = pyqtSignal()
    win_signal = pyqtSignal()
    next_signal = pyqtSignal()
    winner_signal = pyqtSignal()
    
    def __init__(self, s, parentQWidget = None):
        super(Receive, self).__init__(parentQWidget)
        self.parentQWidget = parentQWidget
        self.was_cancelled = False
        self.socket = s

    def run(self):
        while not self.was_cancelled:
            self.connection()

    def die(self):
        self.was_cancelled = True

    @pyqtSlot()
    def connection(self):

            bin = self.socket.recv(2048)
            if(len(bin)) < 20:
                text = str(bin, 'utf-8')
                print(text)      
                if text == 'NEW':
                    self.new_game_signal.emit()
            else:
                frog1 , frog2, vehicles, turtles, logs, level, scores, lives, check_point, timer, turtle_pics, result  = pickle.loads(bin)
                self.position_signal.emit(frog1, frog2, vehicles, turtles, logs, level, scores, lives, check_point,
                                          timer, turtle_pics)
                if result == 'LW':
                    self.lw_signal.emit()
                elif result == 'WL':
                    self.wl_signal.emit()
                elif result == 'LOSER':
                    self.lose_signal.emit()
                elif result == 'WINNER':
                    self.win_signal.emit()
                elif result == 'NEXT':
                    self.next_signal.emit()
                elif result == 'TWINNER':
                    self.winner_signal.emit()
            time.sleep(0.1)


class Send(QObject):
    def __init__(self, s):
        super().__init__()

        self.keys = []
        self.is_done = False
        self.socket = s

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
        #self.thread.quit()

    def __work__(self):
            while not self.is_done:
                k = ''
                text = ''

                if self.keys.__len__() > 0:
                    k = self.keys.pop(0)
                else:
                    continue

                if k == Qt.Key_Right:
                    text = 'right'
                elif k == Qt.Key_Left:
                    text = 'left'
                elif k == Qt.Key_Down:
                    text = 'down'
                elif k == Qt.Key_Up:
                    text = 'up'
                elif k == Qt.Key_W:
                    text = 'w'
                elif k == Qt.Key_S:
                    text = 's'
                elif k == Qt.Key_D:
                    text = 'd'
                elif k == Qt.Key_A:
                    text = 'a'
                elif k == Qt.Key_Escape:
                    break
                self.socket.sendall(text.encode('utf8'))
                time.sleep(0.1)

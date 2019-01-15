from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot, Qt, QMutex
import socket
import time
import pickle

HOST = ''  # The remote host
PORT = 50006  # The same port as used by the server


class CommunicationThreads(QThread):

    connect_signal = pyqtSignal()

    def __init__(self, parentQWidget = None):
        super(CommunicationThreads, self).__init__(parentQWidget)
        self.parenQWidget = parentQWidget
        self.connections = []
        self.was_cancelled = False

    def run(self):
        while not self.was_cancelled:
            print("u runu sam")
            try:
                self.__connect__()
            except Exception as e:
                print("Error:", e)

    def get_last_conn(self):
        if self.connections.__len__() > 0:
            return self.connections.pop(0)
        else:
            return None

    @pyqtSlot()
    def __connect__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((HOST, PORT))
        self.socket.listen(1)
        print("wait for next accept")
        self.conn, self.addr = self.socket.accept()
        print(f"client1 accepted -> address: {self.addr}")
        self.connections.append(self.conn)
        self.connect_signal.emit()


class Receive(QObject):

    key_signal = pyqtSignal(int)

    def __init__(self, c: socket, mode):
        super().__init__()

        self.keys = []
        self.is_done = False
        self.conn = c
        self.m = mode

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

                text = ''
                bin = 0
                try:
                    bin = self.conn.recv(1024)
                except Exception as e:
                    print("Error recv:", e)

                text = str(bin, 'utf-8')
                print('Received', text)
                if self.m == 0:
                    if text == 'right':
                        self.key_signal.emit(Qt.Key_Right)
                    elif text == 'left':
                        self.key_signal.emit(Qt.Key_Left)
                    elif text == 'down':
                        self.key_signal.emit(Qt.Key_Down)
                    elif text == 'up':
                        self.key_signal.emit(Qt.Key_Up)
                    elif text == 'w':
                        self.key_signal.emit(Qt.Key_W)
                    elif text == 'a':
                        self.key_signal.emit(Qt.Key_A)
                    elif text == 's':
                        self.key_signal.emit(Qt.Key_S)
                    elif text == 'd':
                        self.key_signal.emit(Qt.Key_D)
                elif self.m == 1:
                    if text == 'right':
                        self.key_signal.emit(Qt.Key_D)
                    elif text == 'left':
                        self.key_signal.emit(Qt.Key_A)
                    elif text == 'down':
                        self.key_signal.emit(Qt.Key_S)
                    elif text == 'up':
                        self.key_signal.emit(Qt.Key_W)
                else:
                    if text == 'right':
                        self.key_signal.emit(Qt.Key_Right)
                    elif text == 'left':
                        self.key_signal.emit(Qt.Key_Left)
                    elif text == 'down':
                        self.key_signal.emit(Qt.Key_Down)
                    elif text == 'up':
                        self.key_signal.emit(Qt.Key_Up)
                time.sleep(0.1)


class Send(QThread):
    def __init__(self, c: socket, flag, parentQWidget = None):
        super(Send, self).__init__(parentQWidget)
        self.parenQWidget = parentQWidget
        self.was_cancelled = False
        self.conn = c
        self.flag = flag

    def run(self):
        while not self.was_cancelled:
            try:
                self.connect()
            except Exception as e:
                print("Error:", e)

    def connect(self):
            frog1_geo = self.parenQWidget.label1.geometry()
            frog1 = [frog1_geo.x(), frog1_geo.y()]
            frog2_geo = self.parenQWidget.label2.geometry()
            frog2 = [frog2_geo.x(), frog2_geo.y()]

            vehicles = []
            for car in self.parenQWidget.movingCar.vehicles:
                temp_geo = (car.geometry())
                vehicles.append(temp_geo.x())

            turtles = []
            for turtle in self.parenQWidget.movingTurtle.turtles:
                temp_geo = (turtle.geometry())
                turtles.append(temp_geo.x())

            logs = []
            for log in self.parenQWidget.movingLog.logs:
                temp_geo = (log.geometry())
                logs.append(temp_geo.x())

            level = self.parenQWidget.level
            scores = [self.parenQWidget.player1.score, self.parenQWidget.player2.score]
            lives = [self.parenQWidget.player1.lives, self.parenQWidget.player2.lives]

            check_point = []
            for obj in self.parenQWidget.finishObjs:
                if obj.hasFlyBonus is True:
                    check_point.append(2)
                elif obj.finished is True:
                    check_point.append(1)
                else:
                    check_point.append(0)

            self.parenQWidget.mutex.lock()
            timer = self.parenQWidget.timer
            self.parenQWidget.mutex.unlock()
            
            self.parenQWidget.mutex.lock()
            turtle_pic1 = self.parenQWidget.movingTurtle.counter2
            turtle_pic2 = self.parenQWidget.movingTurtle.counter4
            self.parenQWidget.mutex.unlock()
            
            turtle_pics = [turtle_pic1 % 4, turtle_pic2 % 4]
            result = ''
            if self.flag == 0:
                result = self.parenQWidget.result_string0
            elif self.flag == 1:
                result = self.parenQWidget.result_string1
            else:
                result = self.parenQWidget.result_string2
            data = pickle.dumps((frog1, frog2, vehicles, turtles, logs, level, scores, lives, check_point, timer, turtle_pics, result))
            duzina = len(data)
            print("Duzina:", duzina)
            try:
                self.conn.sendall(data)
            except Exception as e:
                print("Error send:", e)
            time.sleep(0.1)

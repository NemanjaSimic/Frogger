from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot
from multiprocessing import Pipe
import time


class FlyBonusThread(QThread):

    zzSignal = pyqtSignal()

    def __init__(self, parentQWidget = None):
        super(FlyBonusThread, self).__init__(parentQWidget)
        self.parent_widget = parentQWidget

        self.was_canceled = False

    def run(self):
        while not self.was_canceled:
            self.readPipe()

    def readPipe(self):
        recvMsg = self.parent_widget.in_pipe.recv()
        self.parent_widget.mutex.lock()

        print("Pipe number", recvMsg)

        if recvMsg == 1 and self.parent_widget.finishObjs[0].finished is False:
            self.parent_widget.finishObjs[0].showBonus()
        elif recvMsg == 2 and self.parent_widget.finishObjs[1].finished is False:
            self.parent_widget.finishObjs[1].showBonus()
        elif recvMsg == 3 and self.parent_widget.finishObjs[2].finished is False:
            self.parent_widget.finishObjs[2].showBonus()
        elif recvMsg == 4 and self.parent_widget.finishObjs[3].finished is False:
            self.parent_widget.finishObjs[3].showBonus()
        elif recvMsg == 5 and self.parent_widget.finishObjs[4].finished is False:
            self.parent_widget.finishObjs[4].showBonus()

        self.parent_widget.mutex.unlock()
        time.sleep(5)
        for finish in self.parent_widget.finishObjs:
            if not finish.finished:
                finish.hideBonus()
from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *
import time


class LogMovement(QObject):

    logMovementSignal = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.is_done = False

        self.thread = QThread()
        self.moveToThread(self.thread)
        self.thread.started.connect(self.__work__)

    def start(self):
        self.thread.start()

    def die(self):
        self.is_done = True
        self.thread.quit()

    @pyqtSlot()
    def __work__(self):
        while not self.is_done:
            self.logMovementSignal.emit()
            time.sleep(0.1)


class LogMoving(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.pix1 = QPixmap('pictures/log_small.png')
        self.pix2 = QPixmap('pictures/log_big.png')
        self.pix3 = QPixmap('pictures/log_medium.png')

        self.logSpeed = 2

        self.labelSmallLog1 = QLabel(self)
        self.labelSmallLog1Obj = MovingLogsObj(self.labelSmallLog1, True, self.logSpeed*0.7)
        self.labelSmallLog2 = QLabel(self)
        self.labelSmallLog2Obj = MovingLogsObj(self.labelSmallLog2, True, self.logSpeed*0.7)
        self.labelSmallLog3 = QLabel(self)
        self.labelSmallLog3Obj = MovingLogsObj(self.labelSmallLog3, True, self.logSpeed*0.7)
        self.labelSmallLog4 = QLabel(self)
        self.labelSmallLog4Obj = MovingLogsObj(self.labelSmallLog4, True, self.logSpeed*0.7)
        self.labelBigLog1 = QLabel(self)
        self.labelBigLog1Obj1 = MovingLogsObj(self.labelBigLog1, True, self.logSpeed*3)
        self.labelBigLog2 = QLabel(self)
        self.labelBigLog1Obj2 = MovingLogsObj(self.labelBigLog2, True, self.logSpeed * 3)
        self.labelBigLog3 = QLabel(self)
        self.labelBigLog1Obj3 = MovingLogsObj(self.labelBigLog3, True, self.logSpeed * 3)
        self.labelBigLog4 = QLabel(self)
        self.labelBigLog1Obj4 = MovingLogsObj(self.labelBigLog4, True, self.logSpeed * 3)
        self.labelMediumLog1 = QLabel(self)
        self.labelMediumLog1Obj = MovingLogsObj(self.labelMediumLog1, True, self.logSpeed)
        self.labelMediumLog2 = QLabel(self)
        self.labelMediumLog2Obj = MovingLogsObj(self.labelMediumLog2, True, self.logSpeed)
        self.labelMediumLog3 = QLabel(self)
        self.labelMediumLog3Obj = MovingLogsObj(self.labelMediumLog3, True, self.logSpeed)
        self.labelMediumLog4 = QLabel(self)
        self.labelMediumLog4Obj = MovingLogsObj(self.labelMediumLog4, True, self.logSpeed)

        self.logsObjs = [self.labelSmallLog1Obj, self.labelSmallLog2Obj, self.labelSmallLog3Obj, self.labelSmallLog4Obj,
                         self.labelBigLog1Obj1, self.labelBigLog1Obj2, self.labelBigLog1Obj3, self.labelBigLog1Obj4,
                         self.labelMediumLog1Obj, self.labelMediumLog2Obj, self.labelMediumLog3Obj, self.labelMediumLog4Obj]

        self.smallLogs = [self.labelSmallLog1, self.labelSmallLog2, self.labelSmallLog3, self.labelSmallLog4]
        self.bigLogs = [self.labelBigLog1, self.labelBigLog2, self.labelBigLog3, self.labelBigLog4]
        self.mediumLogs = [self.labelMediumLog1, self.labelMediumLog2, self.labelMediumLog3, self.labelMediumLog4]

        self.__initPosition__()

        self.logMoving = LogMovement()
        self.logMoving.logMovementSignal.connect(lambda: self.__updatePosition__(self.logSpeed))
        self.logMoving.start()

    def __initPosition__(self):
        self.labelSmallLog1.setPixmap(self.pix1)
        self.labelSmallLog1.setGeometry(0, 245, 91, 27)
        self.labelSmallLog2.setPixmap(self.pix1)
        self.labelSmallLog2.setGeometry(166, 245, 91, 27)
        self.labelSmallLog3.setPixmap(self.pix1)
        self.labelSmallLog3.setGeometry(332, 245, 91, 27)
        self.labelSmallLog4.setPixmap(self.pix1)
        self.labelSmallLog4.setGeometry(492, 245, 91, 27)
        self.labelBigLog1.setPixmap(self.pix2)
        self.labelBigLog1.setGeometry(0, 205, 193, 26)
        self.labelBigLog2.setPixmap(self.pix2)
        self.labelBigLog2.setGeometry(223, 205, 193, 26)
        self.labelBigLog3.setPixmap(self.pix2)
        self.labelBigLog3.setGeometry(446, 205, 193, 26)
        self.labelBigLog4.setPixmap(self.pix2)
        self.labelBigLog4.setGeometry(669, 205, 193, 26)
        self.labelMediumLog1.setPixmap(self.pix3)
        self.labelMediumLog1.setGeometry(0, 125, 125, 27)
        self.labelMediumLog2.setPixmap(self.pix3)
        self.labelMediumLog2.setGeometry(182, 125, 125, 27)
        self.labelMediumLog3.setPixmap(self.pix3)
        self.labelMediumLog3.setGeometry(364, 125, 125, 27)
        self.labelMediumLog4.setPixmap(self.pix3)
        self.labelMediumLog4.setGeometry(546, 125, 125, 27)

        self.show()

    def __updatePosition__(self, logSpeed):
        for smallLog in self.smallLogs:
            smallLogTemp = smallLog.geometry()
            smallLog.setGeometry(smallLogTemp.x() + logSpeed*0.7, smallLogTemp.y(), smallLogTemp.width(), smallLogTemp.height())
            if smallLogTemp.x() >= 571:
                smallLog.setGeometry(-91, 245, 91, 27)

        for bigLog in self.bigLogs:
            bigLogTemp = bigLog.geometry()
            bigLog.setGeometry(bigLogTemp.x() + logSpeed*3, bigLogTemp.y(), bigLogTemp.width(), bigLogTemp.height())
            if bigLogTemp.x() >= 673:
                bigLog.setGeometry(-193, 205, 193, 26)

        for mediumLog in self.mediumLogs:
            mediumLogTemp = mediumLog.geometry()
            mediumLog.setGeometry(mediumLogTemp.x() + logSpeed, mediumLogTemp.y(), mediumLogTemp.width(), mediumLogTemp.height())
            if mediumLogTemp.x() >= 605:
                mediumLog.setGeometry(-125, 125, 125, 27)

    def die(self):
        self.logMoving.die()


class MovingLogsObj:

    def __init__(self, label, smer, brzina):
        self.label = label
        self.smer = smer
        self.brzina = brzina
        self.pluta = True

    def potop(self):
        self.pluta = False

    def plutaj(self):
        self.pluta = True

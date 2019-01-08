import ctypes
from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *
import time
from MovingObjects import MovingObject


class CarMovement(QObject):

    carMovementSignal = pyqtSignal()

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
            self.carMovementSignal.emit()
            time.sleep(0.05)


class CarMoving(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.pix = QPixmap("car_1.png")
        self.labelCar1 = QLabel(self)
        self.labelCar2 = QLabel(self)
        self.labelCar3 = QLabel(self)

        self.carSpeed = 5  # initial speed
        self.__initPosition__()

        self.carMoving = CarMovement()
        self.carMoving.carMovementSignal.connect(lambda: self.__updatePosition__(self.carSpeed))
        self.carMoving.start()

    def __initPosition__(self):
        self.labelCar1.setPixmap(self.pix)
        self.labelCar1.setGeometry(480, 240, 480, 600)
        self.labelCar2.setPixmap(self.pix)
        self.labelCar2.setGeometry(370, 240, 480, 600)
        self.labelCar3.setPixmap(self.pix)
        self.labelCar3.setGeometry(180, 240, 480, 600)
        self.show()

    def __updatePosition__(self, carSpeed):
        car1 = self.labelCar1.geometry()
        car2 = self.labelCar2.geometry()
        car3 = self.labelCar3.geometry()

        self.labelCar1.setGeometry(car1.x() - carSpeed, car1.y(), car1.width(), car1.height())
        self.labelCar2.setGeometry(car2.x() - carSpeed, car2.y(), car2.width(), car2.height())
        self.labelCar3.setGeometry(car3.x() - carSpeed, car3.y(), car3.width(), car3.height())
        if car1.x() == -30:
            self.labelCar1.setGeometry(510, 240, 480, 600)
        if car2.x() == -30:
            self.labelCar2.setGeometry(510, 240, 480, 600)
        if car3.x() == -30:
            self.labelCar3.setGeometry(510, 240, 480, 600)

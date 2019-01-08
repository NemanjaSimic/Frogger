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
        self.pix = QPixmap('car_1.png')
        self.pixTractor = QPixmap('car_2.png')
        self.pixFormula = QPixmap('car_3.png')

        self.labelCar1 = QLabel(self)
        self.labelCar2 = QLabel(self)
        self.labelCar3 = QLabel(self)
        self.labelTractor1 = QLabel(self)
        self.labelTractor2 = QLabel(self)
        self.labelTractor3 = QLabel(self)

        self.labelFormula1 = QLabel(self)
        self.labelFormula2 = QLabel(self)

        self.carSpeed = 2  # initial speed
        self.__initPosition__()

        self.carMoving = CarMovement()
        self.carMoving.carMovementSignal.connect(lambda: self.__updatePosition__(self.carSpeed))
        self.carMoving.start()

    def __initPosition__(self):
        self.labelCar1.setPixmap(self.pix)
        self.labelCar1.setGeometry(480, 520, 40, 40)
        self.labelCar2.setPixmap(self.pix)
        self.labelCar2.setGeometry(370, 520, 40, 40)
        self.labelCar3.setPixmap(self.pix)
        self.labelCar3.setGeometry(180, 520, 40, 40)
        self.labelTractor1.setPixmap(self.pixTractor)
        self.labelTractor1.setGeometry(0, 480, 40, 40)
        self.labelTractor2.setPixmap(self.pixTractor)
        self.labelTractor2.setGeometry(110, 480, 40, 40)
        self.labelTractor3.setPixmap(self.pixTractor)
        self.labelTractor3.setGeometry(300, 480, 40, 40)

        self.labelFormula1.setPixmap(self.pixFormula)
        self.labelFormula1.setGeometry(0, 400, 40, 40)
        self.labelFormula2.setPixmap(self.pixFormula)
        self.labelFormula2.setGeometry(60, 400, 40, 40)

        self.show()

    def __updatePosition__(self, carSpeed):
        car1 = self.labelCar1.geometry()
        car2 = self.labelCar2.geometry()
        car3 = self.labelCar3.geometry()
        car4 = self.labelTractor1.geometry()
        car5 = self.labelTractor2.geometry()
        car6 = self.labelTractor3.geometry()

        car10 = self.labelFormula1.geometry()
        car11 = self.labelFormula2.geometry()

        self.labelCar1.setGeometry(car1.x() - carSpeed, car1.y(), car1.width(), car1.height())
        self.labelCar2.setGeometry(car2.x() - carSpeed, car2.y(), car2.width(), car2.height())
        self.labelCar3.setGeometry(car3.x() - carSpeed, car3.y(), car3.width(), car3.height())
        self.labelTractor1.setGeometry(car4.x() + carSpeed, car4.y(), car4.width(), car4.height())
        self.labelTractor2.setGeometry(car5.x() + carSpeed, car5.y(), car5.width(), car5.height())
        self.labelTractor3.setGeometry(car6.x() + carSpeed, car6.y(), car6.width(), car6.height())

        self.labelFormula1.setGeometry(car10.x() + carSpeed*2, car10.y(), car10.width(), car10.height())
        self.labelFormula2.setGeometry(car11.x() + carSpeed*2, car11.y(), car11.width(), car11.height())

        if car1.x() <= -30:
            self.labelCar1.setGeometry(520, 520, 40, 40)
        if car2.x() <= -30:
            self.labelCar2.setGeometry(520, 520, 40, 40)
        if car3.x() <= -30:
            self.labelCar3.setGeometry(520, 520, 40, 40)
        if car4.x() >= 520:
            self.labelTractor1.setGeometry(-40, 480, 40, 40)
        if car5.x() >= 520:
            self.labelTractor2.setGeometry(-40, 480, 40, 40)
        if car6.x() >= 520:
            self.labelTractor3.setGeometry(-40, 480, 40, 40)

        if car10.x() >= 520:
            self.labelFormula1.setGeometry(-40, 400, 40, 40)
        if car11.x() >= 520:
            self.labelFormula2.setGeometry(-40, 400, 40, 40)

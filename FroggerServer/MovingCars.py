from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *
import time


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
            time.sleep(0.1)


class CarMoving(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.pixCar = QPixmap('pictures/car_1.png')
        self.pixTractor = QPixmap('pictures/car_2.png')
        self.pixFormula = QPixmap('pictures/car_3.png')
        self.pixBPcar = QPixmap('pictures/car_4.png')
        self.pixTruck = QPixmap('pictures/car_5.png')

        self.labelCar1 = QLabel(self)
        self.labelCar2 = QLabel(self)
        self.labelCar3 = QLabel(self)
        self.labelTractor1 = QLabel(self)
        self.labelTractor2 = QLabel(self)
        self.labelTractor3 = QLabel(self)
        self.labelBPcar1 = QLabel(self)
        self.labelBPcar2 = QLabel(self)
        self.labelBPcar3 = QLabel(self)
        self.labelFormula1 = QLabel(self)
        self.labelFormula2 = QLabel(self)
        self.labelTruck1 = QLabel(self)
        self.labelTruck2 = QLabel(self)

        self.cars = [self.labelCar1, self.labelCar2, self.labelCar3]
        self.tractors = [self.labelTractor1, self.labelTractor2, self.labelTractor3]
        self.formulas = [self.labelFormula1, self.labelFormula2]
        self.BPcars = [self.labelBPcar1, self.labelBPcar2, self.labelBPcar3]
        self.trucks = [self.labelTruck1, self.labelTruck2]

        self.vehicle = [self.cars, self.tractors, self.formulas, self.BPcars, self.trucks]

        self.vehicles = []
        for v in self.vehicle:
            for car in v:
                self.vehicles.append(car)

        self.carSpeed = 2  # initial speed
        self.__initPosition__()

        self.carMoving = CarMovement()
        self.carMoving.carMovementSignal.connect(lambda: self.__updatePosition__(self.carSpeed))
        self.carMoving.start()

    def __initPosition__(self):
        self.labelCar1.setPixmap(self.pixCar)
        self.labelCar1.setGeometry(480, 520, 40, 40)
        self.labelCar2.setPixmap(self.pixCar)
        self.labelCar2.setGeometry(370, 520, 40, 40)
        self.labelCar3.setPixmap(self.pixCar)
        self.labelCar3.setGeometry(180, 520, 40, 40)
        self.labelTractor1.setPixmap(self.pixTractor)
        self.labelTractor1.setGeometry(0, 480, 40, 40)
        self.labelTractor2.setPixmap(self.pixTractor)
        self.labelTractor2.setGeometry(110, 480, 40, 40)
        self.labelTractor3.setPixmap(self.pixTractor)
        self.labelTractor3.setGeometry(300, 480, 40, 40)
        self.labelBPcar1.setPixmap(self.pixBPcar)
        self.labelBPcar1.setGeometry(480, 440, 40, 40)
        self.labelBPcar2.setPixmap(self.pixBPcar)
        self.labelBPcar2.setGeometry(370, 440, 40, 40)
        self.labelBPcar3.setPixmap(self.pixBPcar)
        self.labelBPcar3.setGeometry(180, 440, 40, 40)
        self.labelFormula1.setPixmap(self.pixFormula)
        self.labelFormula1.setGeometry(0, 400, 40, 40)
        self.labelFormula2.setPixmap(self.pixFormula)
        self.labelFormula2.setGeometry(60, 400, 40, 40)
        self.labelTruck1.setPixmap(self.pixTruck)
        self.labelTruck1.setGeometry(480, 360, 61, 40)
        self.labelTruck2.setPixmap(self.pixTruck)
        self.labelTruck2.setGeometry(240, 360, 61, 40)

        self.show()

    def __updatePosition__(self, carSpeed):
        for car in self.cars:
            carTemp = car.geometry()
            car.setGeometry(carTemp.x() - carSpeed, carTemp.y(), carTemp.width(), carTemp.height())
            if carTemp.x() <= -40:
                car.setGeometry(520, 520, 40, 40)

        for tractor in self.tractors:
            tractorTemp = tractor.geometry()
            tractor.setGeometry(tractorTemp.x() + carSpeed, tractorTemp.y(), tractorTemp.width(), tractorTemp.height())
            if tractorTemp.x() >= 520:
                tractor.setGeometry(-40, 480, 40, 40)

        for bpcar in self.BPcars:
            bpcarTemp = bpcar.geometry()
            bpcar.setGeometry(bpcarTemp.x() - carSpeed, bpcarTemp.y(), bpcarTemp.width(), bpcarTemp.height())
            if bpcarTemp.x() <= -40:
                bpcar.setGeometry(520, 440, 40, 40)

        for formula in self.formulas:
            formulaTemp = formula.geometry()
            formula.setGeometry(formulaTemp.x() + carSpeed*4, formulaTemp.y(), formulaTemp.width(), formulaTemp.height())
            if formulaTemp.x() >= 520:
                formula.setGeometry(-40, 400, 40, 40)

        for truck in self.trucks:
            truckTemp = truck.geometry()
            truck.setGeometry(truckTemp.x() - carSpeed*0.5, truckTemp.y(), truckTemp.width(), truckTemp.height())
            if truckTemp.x() <= -61:
                truck.setGeometry(541, 360, 61, 40)

    def die(self):
        self.carMoving.die()

    def closeEvent(self, event):
        self.carMoving.die()

    def speed_up(self):
        self.carSpeed += 1
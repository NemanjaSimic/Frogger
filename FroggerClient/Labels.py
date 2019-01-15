from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *
import time


class LogMoving(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.pix1 = QPixmap('pictures/log_small.png')
        self.pix2 = QPixmap('pictures/log_big.png')
        self.pix3 = QPixmap('pictures/log_medium.png')

        self.labelSmallLog1 = QLabel(self)
        self.labelSmallLog2 = QLabel(self)
        self.labelSmallLog3 = QLabel(self)
        self.labelSmallLog4 = QLabel(self)
        self.labelBigLog1 = QLabel(self)
        self.labelBigLog2 = QLabel(self)
        self.labelBigLog3 = QLabel(self)
        self.labelBigLog4 = QLabel(self)
        self.labelMediumLog1 = QLabel(self)
        self.labelMediumLog2 = QLabel(self)
        self.labelMediumLog3 = QLabel(self)
        self.labelMediumLog4 = QLabel(self)

        self.smallLogs = [self.labelSmallLog1, self.labelSmallLog2, self.labelSmallLog3, self.labelSmallLog4]
        self.bigLogs = [self.labelBigLog1, self.labelBigLog2, self.labelBigLog3, self.labelBigLog4]
        self.mediumLogs = [self.labelMediumLog1, self.labelMediumLog2, self.labelMediumLog3, self.labelMediumLog4]

        self.arraysLogs = [self.smallLogs, self.mediumLogs, self.bigLogs]

        self.logs = []
        for arr in self.arraysLogs:
            for log in arr:
                self.logs.append(log)

        self.__initPosition__()

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
        self.__initPosition__()

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

    def close(self):
        self.hide()
        

class TurtleMoving(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.pix3turtlesFull = QPixmap('pictures/turtle_3_full.png')
        self.pix3turtlesHalf = QPixmap('pictures/turtle_3_half.png')
        self.pix3turtlesQuarter = QPixmap('pictures/turtle_3_quarter.png')
        self.pix3turtlesNone = QPixmap('pictures/turtle_3_zero.png')

        self.pix2turtlesFull = QPixmap('pictures/turtle_2_full.png')
        self.pix2turtlesHalf = QPixmap('pictures/turtle_2_half.png')
        self.pix2turtlesQuarter = QPixmap('pictures/turtle_2_quarter.png')
        self.pix2turtlesNone = QPixmap('pictures/turtle_2_zero.png')

        self.labelTurtle1 = QLabel(self)
        self.labelTurtle2 = QLabel(self)
        self.labelTurtle3 = QLabel(self)
        self.labelTurtle4 = QLabel(self)


        self.label2Turtle1 = QLabel(self)
        self.label2Turtle2 = QLabel(self)
        self.label2Turtle3 = QLabel(self)
        self.label2Turtle4 = QLabel(self)

        self.turtles3 = [self.labelTurtle1, self.labelTurtle2, self.labelTurtle3, self.labelTurtle4]
        self.turtlesPictures3 = [self.pix3turtlesFull, self.pix3turtlesHalf, self.pix3turtlesQuarter, self.pix3turtlesNone]
        self.turtles2 = [self.label2Turtle1, self.label2Turtle2, self.label2Turtle3, self.label2Turtle4]
        self.turtlesPictures2 = [self.pix2turtlesFull, self.pix2turtlesHalf, self.pix2turtlesQuarter, self.pix2turtlesNone]

        self.arraysTurtles = [self.turtles3, self.turtles2]
        self.turtles = []
        for arr in self.arraysTurtles:
            for t in arr:
                self.turtles.append(t)

        self.__initPosition__()

    def __initPosition__(self):
        self.labelTurtle1.setPixmap(self.pix3turtlesFull)
        self.labelTurtle1.setGeometry(480, 280, 100, 40)
        self.labelTurtle2.setPixmap(self.pix3turtlesFull)
        self.labelTurtle2.setGeometry(335, 280, 100, 40)
        self.labelTurtle3.setPixmap(self.pix3turtlesFull)
        self.labelTurtle3.setGeometry(190, 280, 100, 40)
        self.labelTurtle4.setPixmap(self.pix3turtlesFull)
        self.labelTurtle4.setGeometry(35, 280, 100, 40)

        self.label2Turtle1.setPixmap(self.pix2turtlesFull)
        self.label2Turtle1.setGeometry(480, 160, 65, 40)
        self.label2Turtle2.setPixmap(self.pix2turtlesFull)
        self.label2Turtle2.setGeometry(328, 160, 65, 40)
        self.label2Turtle3.setPixmap(self.pix2turtlesFull)
        self.label2Turtle3.setGeometry(176, 160, 65, 40)
        self.label2Turtle4.setPixmap(self.pix2turtlesFull)
        self.label2Turtle4.setGeometry(24, 160, 65, 40)

        self.show()

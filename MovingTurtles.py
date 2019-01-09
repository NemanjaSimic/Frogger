from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *
import time


class TurtleMovement(QObject):

    turtleMovementSignal = pyqtSignal()

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
            self.turtleMovementSignal.emit()
            time.sleep(0.1)


class TurtleMoving(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.turtleSpeed = 2

        self.pix3turtlesFull = QPixmap('turtle_3_full.png')
        self.pix3turtlesHalf = QPixmap('turtle_3_half.png')
        self.pix3turtlesQuarter = QPixmap('turtle_3_quarter.png')
        self.pix3turtlesNone = QPixmap('turtle_3_zero.png')

        self.pix2turtlesFull = QPixmap('turtle_2_full.png')
        self.pix2turtlesHalf = QPixmap('turtle_2_half.png')
        self.pix2turtlesQuarter = QPixmap('turtle_2_quarter.png')
        self.pix2turtlesNone = QPixmap('turtle_2_zero.png')

        self.labelTurtle1 = QLabel(self)
        self.labelTurtle1Objs = MovingTurtleObjs(self.labelTurtle1, False, self.turtleSpeed)
        self.labelTurtle2 = QLabel(self)
        self.labelTurtle2Objs = MovingTurtleObjs(self.labelTurtle2, False, self.turtleSpeed)
        self.labelTurtle3 = QLabel(self)
        self.labelTurtle3Objs = MovingTurtleObjs(self.labelTurtle3, False, self.turtleSpeed)
        self.labelTurtle4 = QLabel(self)
        self.labelTurtle4Objs = MovingTurtleObjs(self.labelTurtle4, False, self.turtleSpeed)

        self.label2Turtle1 = QLabel(self)
        self.label2Turtle1Objs = MovingTurtleObjs(self.label2Turtle1, False, self.turtleSpeed*0.5)
        self.label2Turtle2 = QLabel(self)
        self.label2Turtle2Objs = MovingTurtleObjs(self.label2Turtle2, False, self.turtleSpeed*0.5)
        self.label2Turtle3 = QLabel(self)
        self.label2Turtle3Objs = MovingTurtleObjs(self.label2Turtle3, False, self.turtleSpeed*0.5)
        self.label2Turtle4 = QLabel(self)
        self.label2Turtle4Objs = MovingTurtleObjs(self.label2Turtle4, False, self.turtleSpeed*0.5)

        self.turtlesObjs = [self.labelTurtle1Objs, self.labelTurtle2Objs, self.labelTurtle3Objs, self.labelTurtle4Objs,
                            self.label2Turtle1Objs, self.label2Turtle2Objs, self.label2Turtle3Objs,
                            self.label2Turtle4Objs]

        self.turtles3 = [self.labelTurtle1, self.labelTurtle2, self.labelTurtle3, self.labelTurtle4]
        self.turtlesPictures3 = [self.pix3turtlesFull, self.pix3turtlesHalf, self.pix3turtlesQuarter,
                                 self.pix3turtlesNone]
        self.turtles2 = [self.label2Turtle1, self.label2Turtle2, self.label2Turtle3, self.label2Turtle4]
        self.turtlesPictures2 = [self.pix2turtlesFull, self.pix2turtlesHalf, self.pix2turtlesQuarter,
                                 self.pix2turtlesNone]
        # self.turtlesPicturesOther = [self.pix3turtlesFull, self.pix3turtlesHalf] za nogice kornjaca

        self.__initPosition__()
        self.counter = 0
        self.counter2 = 0
        self.counter3 = 0
        self.counter4 = 0

        self.turtleMoving = TurtleMovement()
        self.turtleMoving.turtleMovementSignal.connect(lambda: self.__updatePosition__(self.turtleSpeed))
        self.turtleMoving.start()

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

    def __updatePosition__(self, turtleSpeed):
        for turtle in self.turtles3:
            self.counter = self.counter + 1
            turtleTemp = turtle.geometry()
            turtle.setGeometry(turtleTemp.x() - turtleSpeed, turtleTemp.y(), turtleTemp.width(), turtleTemp.height())
            if turtleTemp.x() <= -100:
                turtle.setGeometry(480, 280, 100, 40)
            if self.counter == 1600:
                self.counter = 0  # reset brojaca
            if self.counter % 16 == 3:
                self.turtlesObjs[2].Plutaj()
                turtle.setPixmap(self.turtlesPictures3[self.counter2 % 4])
                self.counter2 = self.counter2 + 1
                if self.counter2 % 4 == 0:
                    self.counter2 = 0
                    self.turtlesObjs[2].Potop()

        for turtle2 in self.turtles2:
            self.counter3 = self.counter3 + 1
            turtle2Temp = turtle2.geometry()
            turtle2.setGeometry(turtle2Temp.x() - turtleSpeed*0.5, turtle2Temp.y(), turtle2Temp.width(), turtle2Temp.height())
            if turtle2Temp.x() <= -65:
                turtle2.setGeometry(480, 160, 65, 40)
            if self.counter3 == 1600:
                self.counter3 = 0  # reset brojaca
            if self.counter3 % 32 == 3:
                self.turtlesObjs[6].Plutaj()
                turtle2.setPixmap(self.turtlesPictures2[self.counter4 % 4])
                self.counter4 = self.counter4 + 1
                if self.counter4 % 4 == 0:
                    self.counter4 = 0
                    self.turtlesObjs[6].Potop()


class MovingTurtleObjs:

    def __init__(self, label, smer, brzina):
        self.brzina = brzina
        self.label = label
        self.smer = smer
        self.pluta = True

    def Potop(self):
        self.pluta = False

    def Plutaj(self):
        self.pluta = True
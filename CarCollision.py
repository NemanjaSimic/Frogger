from PyQt5.QtCore import *
import time

odstupanje_od_kolizije = 3


class CarCollision(QObject):

    carCollisionSignal = pyqtSignal()

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
            self.carCollisionSignal.emit()
            time.sleep(0.1)


#(frog.y()-odstupanje_od_kolizije >= car_geo.y() and frog.y()+odstupanje_od_kolizije <= (car_geo.y() + car_geo.height()))
class Collision:

    def detect(self):
        frog = self.label1.geometry()
        for veichel in self.movingCar.vehicles:
            for car in veichel:
                car_geo = car.geometry()
                if (((frog.x()-odstupanje_od_kolizije >= car_geo.x() and frog.x()+odstupanje_od_kolizije <= (car_geo.x() + car_geo.width()))
                    or (frog.x()+frog.width()+odstupanje_od_kolizije <= car_geo.x()+car_geo.width() and (frog.x()+frog.width()-odstupanje_od_kolizije >= car_geo.x()))) and frog.y() == car_geo.y() ):
                    self.label1.setGeometry(220, 560, 40, 40)

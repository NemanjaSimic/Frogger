from PyQt5.QtCore import *
import time


odstupanje_od_kolizije = 5


class TurtleCollision(QObject):

    turtleCollisionSignal = pyqtSignal()

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
            self.turtleCollisionSignal.emit()
            time.sleep(0.1)


class CollisionTurtle:
    onTurtle = False

    def detect(self):
        frog = self.label1.geometry()
        self.onTurtle = False
        for log in self.movingTurtle.turtlesObjs:
            log_geo = log.label.geometry()
            if (((frog.x() + odstupanje_od_kolizije >= log_geo.x() and frog.x() - odstupanje_od_kolizije <= (log_geo.x() + log_geo.width()))
                and (frog.x()+frog.width() - odstupanje_od_kolizije <= log_geo.x() + log_geo.width()
                and (frog.x()+frog.width() + odstupanje_od_kolizije >= log_geo.x())))
                    and (frog.y() >= log_geo.y() and frog.y() < (log_geo.y()+log_geo.height()))):
                        if log.pluta:
                            self.moveFrogToRight(frog.x() - log.brzina, frog.y())
                            self.onTurtle = True
                        else:
                            self.label1.setGeometry(220, 560, 40, 40)

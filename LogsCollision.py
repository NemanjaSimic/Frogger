from PyQt5.QtCore import *
import time

odstupanje_od_kolizije = 0


class LogCollision(QObject):

    logCollisionSignal = pyqtSignal()

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
            self.logCollisionSignal.emit()
            time.sleep(0.1)


# and ((frog.y() >= log_geo.y() and frog.y() <=log_geo.y()+log_geo.height()) or (frog.y()+frog.height() < log_geo.y() + log_geo.height()
                        #and frog.y()+frog.height() > log_geo.y()))
class CollisionLog:
    onLog = False

    def detect(self):
        frog = self.label1.geometry()
        self.onLog = False
        for log in self.movingLog.logsObjs:
            log_geo = log.label.geometry()
            if (((frog.x()-odstupanje_od_kolizije >= log_geo.x() and frog.x()+odstupanje_od_kolizije <= (log_geo.x() + log_geo.width()))
                and (frog.x()+frog.width()+odstupanje_od_kolizije <= log_geo.x()+log_geo.width() and (frog.x()+frog.width()-odstupanje_od_kolizije >= log_geo.x())))
                   and (log_geo.y() >= frog.y() and log_geo.y() <= (frog.y()+frog.width()))):
                        self.moveFrogToRight(frog.x()+log.brzina, frog.y())
                        self.onLog = True

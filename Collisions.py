odstupanje_od_kolizije_auta = 10
odstupanje_od_kolizije_log = 0
odstupanje_od_kolizije_turtle = 5


class CarCollision:

    def detect(self):
        frog = self.label1.geometry()
        for vehicle in self.movingCar.vehicles:
            for car in vehicle:
                car_geo = car.geometry()
                if (((frog.x()-odstupanje_od_kolizije_auta >= car_geo.x() and frog.x()-odstupanje_od_kolizije_auta <= (car_geo.x() + car_geo.width()))
                    or (frog.x()+frog.width()-odstupanje_od_kolizije_auta <= car_geo.x()+car_geo.width() and (frog.x()+frog.width()-odstupanje_od_kolizije_auta >= car_geo.x()))) and frog.y() == car_geo.y() ):
                    self.lose_life()


class LogCollision:

    def detect(self):
        frog = self.label1.geometry()
        self.onLog = False
        for log in self.movingLog.logsObjs:
            log_geo = log.label.geometry()
            if (((frog.x()-odstupanje_od_kolizije_log >= log_geo.x() and frog.x()+odstupanje_od_kolizije_log <= (log_geo.x() + log_geo.width()))
                and (frog.x()+frog.width()+odstupanje_od_kolizije_log <= log_geo.x()+log_geo.width() and (frog.x()+frog.width()-odstupanje_od_kolizije_log >= log_geo.x())))
                   and (log_geo.y() >= frog.y() and log_geo.y() <= (frog.y()+frog.width()))):
                        self.moveFrog(frog.x()+log.brzina, frog.y())
                        self.onLog = True


class TurtleCollision:

    def detect(self):
        frog = self.label1.geometry()
        self.onTurtle = False
        for log in self.movingTurtle.turtlesObjs:
            log_geo = log.label.geometry()
            if (((frog.x() + odstupanje_od_kolizije_turtle >= log_geo.x() and frog.x() - odstupanje_od_kolizije_turtle <= (log_geo.x() + log_geo.width()))
                and (frog.x()+frog.width() - odstupanje_od_kolizije_turtle <= log_geo.x() + log_geo.width()
                and (frog.x()+frog.width() + odstupanje_od_kolizije_turtle >= log_geo.x())))
                    and (frog.y() >= log_geo.y() and frog.y() < (log_geo.y()+log_geo.height()))):
                        if log.pluta:
                            self.moveFrog(frog.x() - log.brzina, frog.y())
                            self.onTurtle = True
                        else:
                            self.lose_life()

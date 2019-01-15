odstupanje_od_kolizije_auta = 10
odstupanje_od_kolizije_log = 0
odstupanje_od_kolizije_turtle = 5


class CarCollision:

    def detect(self):
        for player in self.players:
            frog = player.label.geometry()
            for car in self.movingCar.vehicles:
                car_geo = car.geometry()
                if (((frog.x()-odstupanje_od_kolizije_auta >= car_geo.x() and frog.x()-odstupanje_od_kolizije_auta <= (car_geo.x() + car_geo.width()))
                    or (frog.x()+frog.width()-odstupanje_od_kolizije_auta <= car_geo.x()+car_geo.width() and (frog.x()+frog.width()-odstupanje_od_kolizije_auta >= car_geo.x()))) and frog.y() == car_geo.y() ):
                    self.lose_life(player)


class LogCollision:

    def detect(self):
        for player in self.players:
            frog = player.label.geometry()
            player.onLog = False
            for log in self.movingLog.logsObjs:
                log_geo = log.label.geometry()
                if (((frog.x()-odstupanje_od_kolizije_log >= log_geo.x() and frog.x()+odstupanje_od_kolizije_log <= (log_geo.x() + log_geo.width()))
                    and (frog.x()+frog.width()+odstupanje_od_kolizije_log <= log_geo.x()+log_geo.width() and (frog.x()+frog.width()-odstupanje_od_kolizije_log >= log_geo.x())))
                       and (log_geo.y() >= frog.y() and log_geo.y() <= (frog.y()+frog.width()))):
                            self.moveFrog(frog.x()+log.brzina, frog.y(),player)
                            player.onLog = True


class TurtleCollision:

    def detect(self):
        for player in self.players:
            frog = player.label.geometry()
            player.onTurtle = False
            for log in self.movingTurtle.turtlesObjs:
                log_geo = log.label.geometry()
                if (((frog.x() + odstupanje_od_kolizije_turtle >= log_geo.x() and frog.x() - odstupanje_od_kolizije_turtle <= (log_geo.x() + log_geo.width()))
                    and (frog.x()+frog.width() - odstupanje_od_kolizije_turtle <= log_geo.x() + log_geo.width()
                    and (frog.x()+frog.width() + odstupanje_od_kolizije_turtle >= log_geo.x())))
                        and (frog.y() >= log_geo.y() and frog.y() < (log_geo.y()+log_geo.height()))):
                            if log.pluta:
                                self.moveFrog(frog.x() - log.brzina, frog.y(), player)
                                player.onTurtle = True
                            else:
                                self.lose_life(player)

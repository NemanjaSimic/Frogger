from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from multiprocessing import Pipe, Process
import time
import random


class FlyBonus(Process):

    def __init__(self, pipe: Pipe, checkPoints: int):
        super().__init__(target=self.__run__, args=[pipe])
        self.checkPoints = checkPoints

    def __run__(self, pipe: Pipe):
        while True:
            time.sleep(random.randint(5, 10))
            rand_checkPoint = random.randint(1, self.checkPoints)

            pipe.send(rand_checkPoint)
            print("Bravo")

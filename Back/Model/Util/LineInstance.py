from .Consts import *
from numpy import sum


class Line:
    def __init__(self, start_node, end_node, road):
        self.cells = [0]*(10 * road.length // Separation)
        self.road = road
        self.start_node = start_node
        self.end_node = end_node
        self.K = 0
        self.Q = 0
        self.critical_K = Probability / (MaxVelocity + 1 - 2*(1 - Probability))
        #self.cars = []

    def comp(self): # comp density, flow and another things
        self.K = sum(self.cells) / len(self.cells)

        if self.K <= self.critical_K:
            self.Q = (MaxVelocity - 1 + Probability) * self.K

        else:
            self.Q = Probability * (1 - self.K)




    def sortCars(self): # by distance
        pass

    def listCars(self):
        pass

    def __str__(self):
        return str(self.cells)


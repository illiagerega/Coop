from .Consts import *


class Line:
    def __init__(self, start_node, end_node, length):
        self.cells = [0]*(10 * length // Separation)
        self.start_node = start_node
        self.end_node = end_node
        #self.cars = []

    def sortCars(self): # by distance
        pass

    def listCars(self):
        pass

    def __str__(self):
        return str(self.cells)


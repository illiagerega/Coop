Separation = 5


class Line:
    def __init__(self, start_node, end_node, length):
        self.cells = [0]*((length*10) // Separation)
        self.v = start_node
        self.u = end_node
        #self.cars = []

    def sortCars(self): # by distance
        pass

    def listCars(self):
        pass

    def __str__(self):
        return str(self.cells)


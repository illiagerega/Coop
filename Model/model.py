import random
from math import hypot

Separation = 5
types = ['s', 'i']


class Line:
    def __init__(self, start_node, end_node, length):
        self.cells = [0]*(length // Separation)
        self.v = start_node
        self.u = end_node
        #self.cars = []

    def sortCars(self): # by distance
        pass

    def listCars(self):
        pass


class Road:
    def __init__(self, start_node, end_node, number_of_lines):
        self.n_lines = number_of_lines
        self.start_node = start_node
        self.end_node = end_node
        self.length = hypot(start_node.apos[0] - end_node.apos[0], start_node.apos[1] - end_node.apos[1])
        self.lines = [{start_node: []}, {end_node: []}]

        if number_of_lines == 1:
            self.lines[start_node] = [(Line(start_node, end_node, self.length))]
        else:
            for i in range(number_of_lines // 2):
                line = Line(start_node, end_node, self.length)
                self.lines[start_node].append(line)

            for i in range(number_of_lines // 2, number_of_lines):
                line = Line(end_node, start_node, self.length)
                self.lines[end_node].append(line)

class Node:
    def __init__(self, type, apos):
        self.type = types[type] # 'spawn', 'intersect'
        self.apos = apos
        self.start_roads = []
        self.end_roads = []
        self.queue = []

    def addRoad(self, road, type = 'start'):
        if type == 'start':
            self.start_roads.append(road)
        else:
            self.end_roads.append(road)



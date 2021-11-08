from .RoadInstance import Road
from .LineInstance import Line
from .Consts import *
import random
from math import atan, pi, copysign



class Car:
    class WayNode:
        def __init__(self, road_piece: Road, start_node: int, end_node: int):
            self.road = road_piece
            self.start_node = start_node
            self.end_node = end_node

        def __str__(self):
            return str(self.start_node) + " " + str(self.end_node)

    def __init__(self, x, ax=None, ay=None):
        self._v = StartVelocity
        self._a = Acceleration
        self.pause = 0
        self.x = x
        self.apos = [ax, ay]
        self.way = []
        self.wayProgress = -1
        self.currentLine = -1
        self.next_x = -1

    def CompV(self, gap) -> int:
        self._v = min(self._v + self._a, MaxVelocity)
        self._v = min(self._v, gap - 1)
        if random.randint(0, 10) >= Probability * 10:
            self._v = max(self._v - 1, 0)

        return self._v + self.x

    def addWayNode(self, road_piece: Road, start_node: int, end_node: int):
        self.way.append(self.WayNode(road_piece, start_node, end_node))

    def __getNode(self) -> WayNode:
        if 0 <= self.wayProgress < len(self.way):
            return self.way[self.wayProgress]
        else:
            pass

    def getRoad(self) -> Road:
        if 0 <= self.wayProgress < len(self.way):
            return self.__getNode().road
        else:
            pass

    def getLines(self) -> list[Line]:
        if 0 <= self.wayProgress < len(self.way):
            return self.getRoad().lines[self.__getNode().start_node]
        else:
            return []

    def getCoordinates(self) -> [[int, int], int]: # apos, angle

        from .MapController import Map

        current_node = self.__getNode()
        start_node = Map.nodes[current_node.start_node]
        end_node = Map.nodes[current_node.end_node]

        x = end_node.apos[0] - start_node.apos[0]
        y = end_node.apos[1] - start_node.apos[1]

        self.apos[0] = (self.x / len(self.getLines()[0].cells)) * (x) + start_node.apos[0]
        self.apos[1] = (self.x / len(self.getLines()[0].cells)) * (y) + start_node.apos[1]


        return [self.apos, atan(y / x) if x != 0.00 else copysign(pi / 2, y), self._v]
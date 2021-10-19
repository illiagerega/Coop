from .CarInstance import Car
from .RoadInstance import Road


types = ["spawn", "intersect"]


class Node:
    def __init__(self, type, apos):
        self.type = types[type]  # 'spawn', 'intersect'
        self.apos = apos  # absolute position (x, y)
        self.start_roads: list[Road] = []
        self.end_roads: list[Road] = []
        self.queue: list[Car] = []

    def addRoad(self, road: Road, type='start'):
        if type == 'start':
            self.start_roads.append(road)
        else:
            self.end_roads.append(road)

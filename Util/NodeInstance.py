types = ["spawn", "intersect"]


class Node:
    def __init__(self, type, apos):
        self.type = types[type]  # 'spawn', 'intersect'
        self.apos = apos  # absolute position (x, y)
        self.start_roads = []
        self.end_roads = []
        self.queue = []

    def addRoad(self, road, type='start'):
        if type == 'start':
            self.start_roads.append(road)
        else:
            self.end_roads.append(road)

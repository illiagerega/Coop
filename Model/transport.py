import random
import model
from math import inf
from dijkstra import find_shortest_path

Acceleration = 1
StartVelocity = 0
MaxVelocity = 3
Probability = 0.5 # for city - 0.5; for highway - 0.3


class Car:
    def __init__(self, x, ax = None, ay = None):
        self._v = StartVelocity
        self._a = Acceleration
        self.pause = 0
        self.x = x
        self.apos = (ax, ay)
        self.way = []
        self.pos = (None, None)



    def CompV(self, gap):
        self._v = min(self._v + self._a, MaxVelocity)
        self._v = min(self._v, gap - 1)
        if random.randint(0, 10) >= Probability * 10:
            self._v = max(self._v - 1, 0)

        return self._v + self.x

class CarDriver:
    def __init__(self, nodes, roads, n_cars, spawn_nodes, dmat):
        self._cars = []
        self.n_cars = n_cars
        self._spawn_nodes = spawn_nodes
        self.nodes, self.roads = nodes, roads
        self.dmat = dmat
        self.Init()

    def Init(self):
        for i in range(self.n_cars):
            car = Car(-1)
            node = random.choice(self._spawn_nodes)
            self._spawn_nodes.remove(node)
            way = find_shortest_path(self.dmat, node, random.choice(self._spawn_nodes))
            self._spawn_nodes.append(node)

            node.queue.append(car)
            car.way = way # road, v, u
            car.pos = (0, None)



    def Comp(self): # dt = 1 s

        for i in self._spawn_nodes:
            for car in i.queue:
               for line in car.way[0].lines[car.way[1]]:
                   if line.cells[0] != 1:
                        car.x = 0
                        car.pos[1] = car.way[0].lines.indexOf(line)


        for car in self._cars:
            line = car.way[car.pos[0]][0].lines[car.way[car.pos[0]][1]]
            gap = line.cells.indexOf(1, car.x)
            if gap == -1:
                next_x = car.CompV(inf)
            else:
                next_x = car.CompV(gap)

            if next_x >= len(line.cells):
                if car.pos[0] + 1 >= len(car.way):
                    del car
                else:
                    next_x -= line.length
                    line.cells[car.x] = 0
                    car.pos[0] += 1
                    car.pos[1] = random.randrange(len(car.way[car.pos[0]][0].lines[car.way[car.pos[0]][1]]))
                    car.x = next_x
                    car.way[car.pos[0]][0].lines[car.way[car.pos[0]][1]][car.pos[1]].cells[car.x] = 1

            else:
                line.cells[car.x] = 0
                car.pos[0] += 1
                car.pos[1] = random.randrange(len(car.way[car.pos[0]][0].lines[car.way[car.pos[0]][1]]))
                car.x = next_x
                car.way[car.pos[0]][0].lines[car.way[car.pos[0]][1]][car.pos[1]].cells[car.x] = 1




class TrafficLights:
    pass

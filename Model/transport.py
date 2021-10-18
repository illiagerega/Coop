import random
from model import Separation
from math import inf, asin, acos, pi
from dijkstra import find_shortest_path

Acceleration = 1
StartVelocity = 0
MaxVelocity = 3
Probability = 0.5 # for city - 0.5; for highway - 0.3


class Car: # клас для машинок
    def __init__(self, nodes, x, ax = None, ay = None):
        self._v = StartVelocity #
        self._a = Acceleration #
        self.pause = 0 # думаю якійсь делей добавити і тому подібне
        self.x = x # відносна позиція відносно лінії
        self._nodes = nodes # ноди для машинки
        self.apos = [ax, ay] # абсолютні позиції машинок на головних координатах
        self.way = [] # весь шлях, який порахований
        self.pos = [None, None] # відносна позиція машинки ([0] - номер дороги; [1] - вказівник на лінію)



    def CompV(self, gap): # алгоритм для порахування швидкості, відносної дистанції
                          # змінюйте на здоров'я
        self._v = min(self._v + self._a, MaxVelocity)
        self._v = min(self._v, gap - 1)
        if random.randint(0, 10) >= Probability * 10:
            self._v = max(self._v - 1, 0)

        return self._v + self.x

    def Absolute(self): # порахування абсолютної позиції
        line = self.pos[1]
        x = abs(self._nodes[line.u].apos[0] - self._nodes[line.v].apos[0])
        y = abs(self._nodes[line.u].apos[1] - self._nodes[line.v].apos[1])

        self.apos = [ (self.x * x) / (Separation * line.length), (self.x * y) / (Separation * line.length)]
        return [self.apos, 180 * acos(x / line.length) / pi]

class CarDriver: # той, що керує машинками
    def __init__(self, nodes, roads, n_cars, spawn_nodes, dmat):
        self._cars = []
        self.n_cars = n_cars
        self._spawn_nodes = spawn_nodes
        self.nodes, self.roads = nodes, roads
        self.dmat = dmat # матриця дистанцій (для дейкстрі)
        self.Init()

    def Init(self):
        for i in range(self.n_cars):
            car = Car(self.nodes, -1)
            index = random.choice(range(len(self._spawn_nodes)))
            node = self._spawn_nodes[index]
            del self._spawn_nodes[index]
            way = find_shortest_path(self.dmat, node, random.choice(self._spawn_nodes))
            self._spawn_nodes.insert(index, node)

            self.nodes[self._spawn_nodes[index]].queue.append(car)
            car.way = way # road, v, u
            car.pos = [0, None]

            self._cars.append(car)



    def Comp(self): # dt = 1 s


        # Spawn nodes: перевірка на черги машинок, так як тільки що заспавнені машинки
        # не можуть сразу попасти на дорогу; буде накладанння
        for i in self._spawn_nodes:
            for car in self.nodes[i].queue:
               for line in car.way[0][0].lines[car.way[0][1]]:
                   if line.cells[0] != 1:
                        car.x = 0
                        car.pos[1] = line
                        line.cells[0] = 1
                        self.nodes[i].queue.remove(car)


        for car in self._cars:
            if car.x == -1: # машина в черзі
                continue
            line = car.pos[1]
            try:
                gap = line.cells.index(1, car.x + 1)
                next_x = car.CompV(gap)
            except:
                next_x = car.CompV(inf)


            if next_x >= len(line.cells): # якщо машина виїхджає з лінії
                if car.pos[0] + 1 >= len(car.way):
                    del car
                else:
                    next_x -= line.length
                    line.cells[car.x] = 0
                    car.pos[0] += 1
                    car.pos[1] = random.choice(car.way[car.pos[0]][0].lines[car.way[car.pos[0]][1]])
                    # Ця страхопудина вертає (рандомну) лінію, не має світлофорів і перевірки на черг
                    # і тому подібне; треба переписувати
                    car.x = next_x

                    car.pos[1].cells[car.x] = 1

            else: # якщо є ні
                line.cells[car.x] = 0
                car.x = next_x
                line.cells[car.x] = 1


    def ReturnCarPos(self): # вертає позиції машинок
        pos = []

        for car in self._cars:
            if car.x != -1:
                pos.append(car.Absolute())

        return pos

    def ReturnRelativeCarPos(self): # вертає відносні позиції (car.x)
        pos = []

        for car in self._cars:
            if car.x != -1:
                pos.append(car.x)

        return pos



class TrafficLights: # Світлофори
    pass

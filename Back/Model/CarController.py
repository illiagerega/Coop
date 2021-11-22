from .Util.Algorithms import GraphAlgorithms
from .Util.CarInstance import Car
from .Util.MapController import Map
from .Util.RoadInstance import Road
from .Util.LineInstance import Line
from .Util.Consts import NameCarsFile
import os
import random
import json
from math import inf


class CarDriver:
    cars_array: list[Car] = []

    @staticmethod
    def init():
        CarDriver.cars_array = []
        print(Map.n_cars)
        for i in range(Map.n_cars):
            node = random.choice(Map.spawn_nodes)
            way = GraphAlgorithms.dijkstra(Map.distance_matrix, node, random.choice([i for i in Map.spawn_nodes if i != node]))

            pos = (0, None)

            car = Car(-1)
            for x in way:
                car.addWayNode(x[0], x[1], x[2])
            car.pos = pos

            Map.nodes[node].queue.append(car)
            CarDriver.cars_array.append(car)

            CarDriver.assignCars()

    @staticmethod
    def assignCars():
        for spawn_node in Map.spawn_nodes:
            queue_del = []
            for car in Map.nodes[spawn_node].queue:
                car.wayProgress = 0
                for line in car.getLines():
                    if line.cells[0] == 0:
                        car.x = 0
                        line.cells[0] = 1
                        queue_del.append(car)

                Map.nodes[spawn_node].queue = [temp for temp in Map.nodes[spawn_node].queue if not (temp in queue_del) ]



    @staticmethod
    def comp():  # dt = 1 s

        CarDriver.assignCars()

        for car_index, car in enumerate(CarDriver.cars_array):
            if car.x == -1:
                continue

            line = car.getLines()[car.currentLine]
            try:
                gap = line.cells.index(1, car.x + 1) - car.x
                if gap == -1:
                    car.next_x = car.CompV(max(3, len(line.cells) - car.x))
                else:
                    car.next_x = car.CompV(gap)
            except ValueError:
                car.next_x = car.CompV(max(3, len(line.cells) - car.x))


        for car_index, car in enumerate(CarDriver.cars_array):



            if car.x == -1:
                continue

            line = car.getLines()[car.currentLine]
            line.cells[car.x] = 0
            if car.next_x >= len(line.cells):
                if car.wayProgress + 1 >= len(car.way):
                    del CarDriver.cars_array[car_index]
                    del car
                    continue
                else:
                    car.next_x -= len(line.cells)
                    car.wayProgress += 1

            car.currentLine = random.randrange(len(car.getLines()))
            car.x = car.next_x
            car.getLines()[car.currentLine].cells[car.x] = 1

    def __get_path(u, v):
        return GraphAlgorithms.dijkstra(Map.distance_matrix, u, v)

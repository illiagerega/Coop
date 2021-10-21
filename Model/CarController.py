from Util.dijkstra import find_shortest_path
from Util.CarInstance import Car
from Util.MapController import Map
from Util.RoadInstance import Road
from Util.LineInstance import Line
import random
import json
from math import inf


class CarDriver:
    cars_array: list[Car] = []

    @staticmethod
    def init():
        print(Map.n_cars)
        for i in range(Map.n_cars):
            node = random.choice(Map.spawn_nodes)
            way = find_shortest_path(Map.distance_matrix, node, random.choice([i for i in Map.spawn_nodes if i != node]))
           # way = find_shortest_path(Map.distance_matrix, 0, 4)
            print(node)
            print("DKJFDSLKFJDSKLFJDSKLFJDSKL")

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
            for car in Map.nodes[spawn_node].queue:
                car.wayProgress = 0
                assigned = False

                print(car.way)
                for i in range(0, len(car.getLines()[0].cells), 2):
                    for index, line in enumerate(car.getLines()):
                        if line.cells[i] == 0:
                            line.cells[i] = 1
                            print("Assign " + str(i))
                            car.x = i
                            car.currentLine = index
                            assigned = True
                    if assigned:
                        break

            Map.nodes[spawn_node].queue.clear()

    @staticmethod
    def comp():  # dt = 1 s

        for car_index, car in enumerate(CarDriver.cars_array):
            line = car.getLines()[car.currentLine]
            try:
                gap = line.cells.index(1, car.x + 1)
                if gap == -1:
                    car.next_x = car.CompV(max(3, len(line.cells) - car.x))
                else:
                    car.next_x = car.CompV(gap)
            except ValueError:
                car.next_x = car.CompV(max(3, len(line.cells) - car.x))


        for car_index, car in enumerate(CarDriver.cars_array):

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

    def getEverythingIntoFile(self): # print coordinates into file .json
        pass

    def __get_path(u, v):
        return find_shortest_path(Map.distance_matrix, u, v)

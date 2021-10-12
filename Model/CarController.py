from Util.dijkstra import find_shortest_path
from Util.CarInstance import Car
from Util.MapController import Map
import random
from math import inf


class CarDriver:
    cars_array = []

    @staticmethod
    def init():
        print(Map.n_cars)
        for i in range(Map.n_cars):
            node = random.choice(Map.spawn_nodes)
            way = find_shortest_path(Map.distance_matrix, node, random.choice([i for i in Map.spawn_nodes if i != node]))
            pos = (0, None)

            car = Car(-1)
            car.way = way
            car.pos = pos

            Map.nodes[node].queue.append(car)
            CarDriver.cars_array.append(car)

    @staticmethod
    def comp(self):  # dt = 1 s

        for i in Map.spawn_nodes:
            for car in i.queue:
                for line in car.way[0].lines[car.way[1]]:
                    if line.cells[0] != 1:
                        car.x = 0
                        car.pos[1] = car.way[0].lines.indexOf(line)

        for car in self.cars:
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

    def __get_path(u, v):
        return find_shortest_path(Map.distance_matrix, u, v)

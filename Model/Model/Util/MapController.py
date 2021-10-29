from .RoadInstance import Road
from .NodeInstance import Node
from .Consts import NameMapFile
import json


class Map:

    n_nodes: int
    n_roads: int
    n_cars: int
    nodes: list[Node] = []
    spawn_nodes: list[int] = []
    roads: list[Road] = []
    distance_matrix = []

    @staticmethod
    def get_distances():
        Map.distance_matrix = []
        # k = 0
        for i in range(Map.n_nodes):
            temp = []
            for j in range(Map.n_nodes):
                temp.append([0, None])
            Map.distance_matrix.append(temp)

        for index, node in enumerate(Map.nodes):
            for road in node.start_roads:
                Map.distance_matrix[road.start_node][road.end_node] = [road.length, road]

        # for i in Map.distance_matrix:
        #     print(i)

        # for line in Map.distance_matrix:
        #     print(line)

    @staticmethod
    def init(Ncars):
        Map.n_nodes = len(Map.nodes)
        Map.n_roads = len(Map.roads)
        Map.n_cars = Ncars
        Map.get_distances()


from .RoadInstance import Road
from .NodeInstance import Node
from .Consts import NameMapFile, NCars
import json


class Map:

    n_nodes: int
    n_roads: int
    n_cars: int
    nodes: list[Node] = []
    spawn_nodes: list[int]
    roads: list[Road] = []
    distance_matrix = []

    @staticmethod
    def get_distances():
        Map.distance_matrix = []
        k = 0
        for node in Map.nodes:
            mat = [[0, None]] * len(Map.nodes)
            for i in node.start_roads:
                if i.end_node != k:
                    mat[i.end_node] = [i.length, i]
                elif i.start_node != k and i.lines != 1:
                    mat[i.start_node] = [i.length, i]
                else:
                    pass

            Map.distance_matrix.append(mat)
            k += 1

        # for line in Map.distance_matrix:
        #     print(line)

    @staticmethod
    def init(nodes, spawn_nodes, roads):
        Map.n_nodes = len(nodes)
        Map.n_roads = len(roads)
        Map.n_cars = NCars
        Map.nodes = nodes
        Map.roads = roads
        Map.spawn_nodes = spawn_nodes
        Map.get_distances()


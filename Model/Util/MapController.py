from .RoadInstance import Road
from .NodeInstance import Node
from .Consts import NameMapFile
import json


class Map:

    n_nodes: int
    n_road: int
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
    def init(fileName):

        graph = open(fileName, 'r')

        Map.n_nodes, Map.n_roads, Map.n_cars = list(map(int, graph.readline().split()))

        Map.nodes = [None] * Map.n_nodes
        Map.spawn_nodes = []
        Map.roads = [None] * Map.n_roads

        for i in range(Map.n_nodes):
            type_name, x, y = list(map(int, graph.readline().split()))  # types: 0 - spawn, 1 - intersect
            node = Node(type_name, (x, y), i)
            Map.nodes[i] = node

            if type_name == 0:
                Map.spawn_nodes.append(i)

        for i in range(Map.n_roads):
            s_n, e_n, n_lines = list(
                map(int, graph.readline().split()))  # start node, end node, length, number of lines, absolute position
            road = Road(Map.nodes, s_n, e_n, n_lines)
            Map.roads[i] = road

            Map.nodes[s_n].addRoad(road)
            Map.nodes[e_n].addRoad(road, 'end')

            if n_lines > 1:
                Map.nodes[e_n].addRoad(road)
                Map.nodes[s_n].addRoad(road, 'end')

        Map.get_distances()
        # spawn_point, end_point = list(map(int, input().split()))

        # way = list(map(int, input().split()))


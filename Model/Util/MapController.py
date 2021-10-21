from .RoadInstance import Road
from .NodeInstance import Node


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
        # This has to be bidirectional
        for i in range(Map.n_nodes):
            temp= []
            for j in range(Map.n_nodes):
                temp.append([0, None])
            Map.distance_matrix.append(temp)

        for index, node in enumerate(Map.nodes):
            for road in node.start_roads:
                Map.distance_matrix[road.start_node][road.end_node] = [road.length, road]

        for i in Map.distance_matrix:
            print(i)


    @staticmethod
    def init(fileName):

        graph = open(fileName, 'r')

        Map.n_nodes, Map.n_roads, Map.n_cars = list(map(int, graph.readline().split()))

        Map.nodes = [None] * Map.n_nodes
        Map.spawn_nodes = []
        Map.roads = [None] * Map.n_roads

        for i in range(Map.n_nodes):
            type_name, x, y = list(map(int, graph.readline().split()))  # types: 0 - spawn, 1 - intersect
            node = Node(type_name, (x, y))
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
                # Це якись убогий костиль, треба якось його забрати, но поки що і так сойдет
                # (поки що, робим вигляд шо у нас або 1 або 2 лінії (одностороннє або двухстороннє))
                reverse_road = Road(Map.nodes, e_n, s_n, n_lines)
                Map.nodes[e_n].addRoad(reverse_road)
                Map.nodes[s_n].addRoad(reverse_road, 'end')

        Map.get_distances()
        # spawn_point, end_point = list(map(int, input().split()))

        # way = list(map(int, input().split()))

from .Util.MapController import Map
from .CarController import CarDriver
from .LightsController import LightsController
from .Util.NodeInstance import Node
from .Util.RoadInstance import Road
from .Util.Consts import *

import json
import osmnx

class PortDriver:

    @staticmethod
    def getCarsIntoFile(): # cars into file.json for simulation
        export_file = open(NameCarsFile, 'w')

        row = []

        for car_index, car in enumerate(CarDriver.cars_array):
            if car.x != -1:
                row.append({ car_index : car.getCoordinates()} )

        json.dump({"cars": row}, export_file)

        export_file.close()

    @staticmethod
    def getMapIntoFile():  # all graph into file.json for simulation
        export_file = open(NameMapFile, 'w')

        row_nodes = []
        row_roads = {}

        for node in Map.nodes:
            row_nodes.append([node.apos, node.type])
            temp = {}
            for road in node.start_roads:
                temp[road.end_node] = [road.n_lines, road.angle]

            row_roads.append(temp)




        json.dump({"nodes": row_nodes, "roads": row_roads}, export_file)
        export_file.close()


    @staticmethod
    def setMapByName(Name):
        graph = osmnx.graph_from_place(Name, simplify=True)

        Map.nodes = []
        Map.roads = []
        Map.spawn_nodes = []
        nodes_indexes = {}
        roads_to_delete = []

        # print(graph.roads(0))
        offset_x = graph.nodes[next(iter(graph.nodes))]['x']
        offset_y = graph.nodes[next(iter(graph.nodes))]['y']

        for node_index, node in enumerate(graph.nodes):
            attributes = graph.nodes[node]
            Map.nodes.append(
                Node(0, [(attributes['x'] - offset_x) * Scale, (attributes['y'] - offset_y) * Scale], node_index))
            Map.nodes[-1].attributes = attributes
            if Map.nodes[-1].type == "spawn":
                Map.spawn_nodes.append(node)

            nodes_indexes[node] = node_index
            pass

        nodes_n_roads = [0] * len(Map.nodes)
        for edge in graph.edges:
            attributes = graph.edges[edge]
            if 'highway' in attributes:
                if attributes['highway'] in ForbiddenHighways:
                    roads_to_delete.append(edge)
                    print(Map.nodes[nodes_indexes[edge[0]]])
                    print(Map.nodes[nodes_indexes[edge[1]]])
                    continue
            else:
                roads_to_delete.append(edge)
                continue

            nodes_n_roads[nodes_indexes[edge[0]]] += 1
            nodes_n_roads[nodes_indexes[edge[1]]] += 1

        for edge in roads_to_delete:
            graph.remove_edge(edge[0], edge[1], edge[2])

        Map.nodes = [Map.nodes[i] for i in range(len(Map.nodes)) if nodes_n_roads[i] != 0]
        nodes_indexes = {i: nodes_indexes[i] for i in nodes_indexes if nodes_n_roads[nodes_indexes[i]] != 0}
        for node_index, node in enumerate(Map.nodes):
            node.index = node_index

        for index, node_index in enumerate(nodes_indexes.keys()):
            nodes_indexes[node_index] = index

        Map.spawn_nodes = range(len(Map.nodes))

        roads_to_delete = None
        for edge in graph.edges:
            attributes = graph.edges[edge]
            s_n = nodes_indexes[edge[0]]
            e_n = nodes_indexes[edge[1]]
            lanes = (int(attributes['lanes']) if not isinstance(attributes['lanes'], list) else int(
                attributes['lanes'][0])) if 'lanes' in attributes.keys() else 1
            Map.roads.append(Road(Map.nodes, s_n, e_n, (lanes + 1) // 2))
            Map.nodes[s_n].addRoad(Map.roads[-1])
            Map.nodes[e_n].addRoad(Map.roads[-1], 'end')

            # if roads[-1].n_lines > 1:
            #     nodes[e_n].addRoad(roads[-1])
            #     nodes[s_n].addRoad(roads[-1], 'end')

        graph = None
        # Map.init(nodes, spawn_nodes, roads)
        return [Map.nodes, Map.spawn_nodes, Map.roads]

    @staticmethod
    def setMapFromFile(fileName):

        if '.json' in fileName:
            import_file = open(fileName, 'r')

            data = json.load(import_file)

            row_nodes = data['nodes']
            row_roads = data['roads']

            Map.nodes = []
            Map.roads = []
            Map.spawn_nodes = []

            for node_index, node in enumerate(row_nodes):
                Map.nodes.append(Node(node[1], node[0], node_index))
                if Map.nodes[-1].type == 0:
                    Map.spawn_nodes.append(Map.nodes[-1].index)


            for road in row_roads:
                s_n = road[0][0]
                e_n = road[0][1]
                Map.roads.append(Road(Map.nodes, s_n, e_n, road[1]))
                Map.nodes[s_n].addRoad(Map.roads[-1])
                Map.nodes[e_n].addRoad(Map.roads[-1], 'end')

            #Map.init(nodes, spawn_nodes, roads)
            import_file.close()
            return [Map.nodes, Map.spawn_nodes, Map.roads]


        elif '.osm' in fileName: # from .osm
            graph = osmnx.graph_from_xml(fileName, simplify=True)

            Map.nodes = []
            Map.roads = []
            Map.spawn_nodes = []
            nodes_indexes = {}
            roads_to_delete = []

            #print(graph.roads(0))
            offset_x = graph.nodes[next(iter(graph.nodes))]['x']
            offset_y = graph.nodes[next(iter(graph.nodes))]['y']

            for node_index, node in enumerate(graph.nodes):
                attributes = graph.nodes[node]
                Map.nodes.append(Node(0, [(attributes['x'] - offset_x) * Scale, (attributes['y'] - offset_y) * Scale], node_index))
                Map.nodes[-1].attributes = attributes
                if Map.nodes[-1].type == "spawn":
                    Map.spawn_nodes.append(node)

                nodes_indexes[node] = node_index
                pass

            nodes_n_roads = [0] * len(Map.nodes)
            for edge in graph.edges:
                attributes = graph.edges[edge]
                if 'highway' in attributes:
                    if attributes['highway'] in ForbiddenHighways:
                        roads_to_delete.append(edge)
                        print(Map.nodes[nodes_indexes[edge[0]]])
                        print(Map.nodes[nodes_indexes[edge[1]]])
                        continue
                else:
                    roads_to_delete.append(edge)
                    continue

                nodes_n_roads[nodes_indexes[edge[0]]] += 1
                nodes_n_roads[nodes_indexes[edge[1]]] += 1

            for edge in roads_to_delete:
                graph.remove_edge(edge[0], edge[1], edge[2])

            Map.nodes = [Map.nodes[i] for i in range(len(Map.nodes)) if nodes_n_roads[i] != 0]
            nodes_indexes = { i : nodes_indexes[i] for i in nodes_indexes if nodes_n_roads[nodes_indexes[i]] != 0}
            for node_index, node in enumerate(Map.nodes):
                node.index = node_index

            for index, node_index in enumerate(nodes_indexes.keys()):
                nodes_indexes[node_index] = index

            Map.spawn_nodes = range(len(Map.nodes))

            roads_to_delete = None
            for edge in graph.edges:
                attributes = graph.edges[edge]
                s_n = nodes_indexes[edge[0]]
                e_n = nodes_indexes[edge[1]]
                lanes = (int(attributes['lanes']) if not isinstance(attributes['lanes'], list) else int(attributes['lanes'][0])) if 'lanes' in attributes.keys() else 1
                Map.roads.append(Road(Map.nodes, s_n, e_n, (lanes + 1) // 2 ))
                Map.nodes[s_n].addRoad(Map.roads[-1])
                Map.nodes[e_n].addRoad(Map.roads[-1], 'end')


                # if roads[-1].n_lines > 1:
                #     nodes[e_n].addRoad(roads[-1])
                #     nodes[s_n].addRoad(roads[-1], 'end')

            graph = None
            #Map.init(nodes, spawn_nodes, roads)
            return [Map.nodes, Map.spawn_nodes, Map.roads]

        else: # from .txt
            graph = open(fileName, 'r')

            n_nodes, n_roads, n_cars = list(map(int, graph.readline().split()))

            Map.nodes = [None] * n_nodes
            Map.spawn_nodes = []
            Map.roads = [None] * n_roads

            for i in range(n_nodes):
                type_name, x, y = list(map(int, graph.readline().split()))  # types: 0 - spawn, 1 - intersect
                node = Node(type_name, (x, y), i)
                Map.nodes[i] = node

                if type_name == 0:
                    Map.spawn_nodes.append(i)

            for i in range(n_roads):
                s_n, e_n, n_lines = list(
                    map(int,
                        graph.readline().split()))  # start node, end node, length, number of lines, absolute position
                road = Road(Map.nodes, s_n, e_n, n_lines // 2 if n_lines > 1 else n_lines)
                Map.roads[i] = road

                Map.nodes[s_n].addRoad(road)
                Map.nodes[e_n].addRoad(road, 'end')

                if n_lines > 1:
                    reverse_road = Road(Map.nodes, e_n, s_n, n_lines // 2)
                    Map.roads.append(reverse_road)
                    Map.nodes[e_n].addRoad(reverse_road)
                    Map.nodes[s_n].addRoad(reverse_road, 'end')

            graph = None
            #Map.init(nodes, spawn_nodes, roads)
            return [Map.nodes, Map.spawn_nodes, Map.roads]

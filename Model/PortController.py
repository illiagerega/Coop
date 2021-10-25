from Util.MapController import Map
from CarController import CarDriver
from LightsController import LightsController
from Util.NodeInstance import Node
from Util.RoadInstance import Road
from Util.Consts import *

import json
import osmnx

class PortDriver:

    @staticmethod
    def getCarsIntoFile(): # cars into file.json for simulation
        export_file = open(NameCarsFile, 'w')

        row = []

        for car_index, car in enumerate(CarDriver.cars_array):
            row.append(car.getCoordinates(), )

        json.dump({"cars": row}, export_file)

        export_file.close()

    @staticmethod
    def getMapIntoFile():  # all graph into file.json for simulation
        export_file = open(NameMapFile, 'w')

        row_nodes = []
        row_roads = []

        for node in Map.nodes:
            row_nodes.append([node.apos, node.type])

        for index_road, road in enumerate(Map.roads):
            row_roads.append([(road.start_node, road.end_node), road.n_lines])

        json.dump({"nodes": row_nodes, "roads": row_roads}, export_file)
        export_file.close()





    @staticmethod
    def setMapFromFile(fileName):

        if '.json' in fileName:
            import_file = open(fileName, 'r')

            data = json.load(import_file)

            row_nodes = data['nodes']
            row_roads = data['roads']

            nodes = []
            spawn_nodes = []
            roads = []

            for node_index, node in enumerate(row_nodes):
                nodes.append(Node(node[1], node[0], node_index))
                if nodes[-1].type == 0:
                    spawn_nodes.append(nodes[-1].index)


            for road in row_roads:
                s_n = road[0][0]
                e_n = road[0][1]
                roads.append(Road(nodes, s_n, e_n, road[1]))
                nodes[s_n].addRoad(roads[-1])
                nodes[e_n].addRoad(roads[-1], 'end')

            Map.init(nodes, spawn_nodes, roads)
            return [nodes, spawn_nodes, roads]


        elif '.osm' in fileName: # from .osm
            graph = osmnx.graph_from_xml(fileName)
            nodes = []
            spawn_nodes = []
            nodes_indexes = {}
            roads = []
            roads_to_delete = []

            #print(graph.roads(0))
            offset_x = graph.nodes[next(iter(graph.nodes))]['x']
            offset_y = graph.nodes[next(iter(graph.nodes))]['y']

            for node_index, node in enumerate(graph.nodes):
                attributes = graph.nodes[node]
                nodes.append(Node(0, [(attributes['x'] - offset_x) * Scale, (attributes['y'] - offset_y) * Scale], node_index))
                if nodes[-1].type == "spawn":
                    spawn_nodes.append(node)

                nodes_indexes[node] = node_index
                pass

            nodes_n_roads = [0] * len(nodes)
            for edge in graph.edges:
                attributes = graph.edges[edge]
                if 'highway' in attributes:
                    if attributes['highway'] in ForbiddenHighways:
                        roads_to_delete.append(edge)
                        continue
                else:
                    roads_to_delete.append(edge)
                    continue

                nodes_n_roads[nodes_indexes[edge[0]]] += 1
                nodes_n_roads[nodes_indexes[edge[1]]] += 1

            for edge in roads_to_delete:
                graph.remove_edge(edge[0], edge[1], edge[2])

            nodes = [nodes[i] for i in range(len(nodes)) if nodes_n_roads[i] != 0]
            nodes_indexes = { i : nodes_indexes[i] for i in nodes_indexes if nodes_n_roads[nodes_indexes[i]] != 0}
            for node_index, node in enumerate(nodes):
                node.index = node_index

            for index, node_index in enumerate(nodes_indexes.keys()):
                nodes_indexes[node_index] = index

            spawn_nodes = range(len(nodes))

            for edge in graph.edges:
                attributes = graph.edges[edge]
                s_n = nodes_indexes[edge[0]]
                e_n = nodes_indexes[edge[1]]
                roads.append(Road(nodes, s_n, e_n, (int(attributes['lanes']) + 1) // 2 if 'lanes' in attributes.keys() else 1))
                nodes[s_n].addRoad(roads[-1])
                nodes[e_n].addRoad(roads[-1], 'end')


                # if roads[-1].n_lines > 1:
                #     nodes[e_n].addRoad(roads[-1])
                #     nodes[s_n].addRoad(roads[-1], 'end')


            Map.init(nodes, spawn_nodes, roads)
            return [nodes, spawn_nodes, roads]

        else: # from .txt
            graph = open(fileName, 'r')

            n_nodes, n_roads, n_cars = list(map(int, graph.readline().split()))

            nodes = [None] * n_nodes
            spawn_nodes = []
            roads = [None] * n_roads

            for i in range(n_nodes):
                type_name, x, y = list(map(int, graph.readline().split()))  # types: 0 - spawn, 1 - intersect
                node = Node(type_name, (x, y), i)
                nodes[i] = node

                if type_name == 0:
                    spawn_nodes.append(i)

            for i in range(n_roads):
                s_n, e_n, n_lines = list(
                    map(int,
                        graph.readline().split()))  # start node, end node, length, number of lines, absolute position
                road = Road(nodes, s_n, e_n, n_lines // 2 if n_lines > 1 else n_lines)
                roads[i] = road

                nodes[s_n].addRoad(road)
                nodes[e_n].addRoad(road, 'end')

                if n_lines > 1:
                    reverse_road = Road(nodes, e_n, s_n, n_lines // 2)
                    roads.append(reverse_road)
                    nodes[e_n].addRoad(reverse_road)
                    nodes[s_n].addRoad(reverse_road, 'end')

            Map.init(nodes, spawn_nodes, roads)
            return [nodes, spawn_nodes, roads]

from .Util.MapController import Map
from .CarController import CarDriver
from .LightsController import LightsController
from .Util.NodeInstance import Node
from .Util.RoadInstance import Road
from .Util.Consts import *
from .Util.Algorithms import excludeOSMGraph
from .config import *

import json
import osmnx

class PortDriver:

    @staticmethod
    def getCarsIntoFile(): # cars into file.json for simulation
        row = []

        for car_index, car in enumerate(CarDriver.cars_array):
            if car.x != -1:
                row.append({ car_index : [car.getCoordinates(), car]} )

        data = json.dumps({"cars": row})
        
        return data
        #print(data)
        # ServerRabbit.sendData(data, 'cars')

    @staticmethod
    def getMapIntoFile():  # all graph into file.json for simulation
        row_nodes = []
        row_roads = {}

        for node in Map.nodes:
            row_nodes.append([node.apos, node.type])
            temp = {}
            for road in node.start_roads:
                temp[road.end_node] = [road.n_lines, road.angle]

            row_roads[node.index] = temp

        # data = json.dumps({"nodes": row_nodes, "roads": row_roads})


        return {"nodes": row_nodes, "roads": row_roads}
        # ServerRabbit.sendData(data, 'cars') 


    @staticmethod
    def setMapByName(Name):
        graph = osmnx.graph_from_place(Name, simplify=True)

        Map.nodes, Map.spawn_nodes, Map.roads = excludeOSMGraph(graph)

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

            Map.nodes, Map.spawn_nodes, Map.roads = excludeOSMGraph(graph)

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

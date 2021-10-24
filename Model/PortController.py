from Util.MapController import Map
from CarController import CarDriver
from LightsController import LightsController
from Util.Consts import *

import json
import osm2geojson

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
    def setMapFromFile(osm=False): # in development
        if not osm:
            import_file = open(NameMapFile, 'r')

            data = json.load(import_file)

            row_nodes = data['nodes']
            row_roads = data['roads']

            #for node_index, node in enumerate(row_nodes):
        else:
            import_file = open(NameOsmFile, 'r')
            import_string = import_file.readlines()
            xml_string = ""
            for string in import_string:
                xml_string += string.split('\n')[0]

            data = osm2geojson.xml2geojson(xml_string)
            data = json.loads(data)
            print(data)
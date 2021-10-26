from random import randrange
from .Util.TrafficLightInstance import TrafficLight
from .Util.MapController import Map
from .Util.Consts import StartPeriodLow, StartPeriodHigh

class LightsController:

    traffic_lights : list[TrafficLight] = []

    @staticmethod
    def init():


        for node_index, node in enumerate(Map.nodes):
            if node.type != 'intersect' or len(node.end_roads) < 2:
                continue


            LightsController.traffic_lights.append(TrafficLight(node.end_roads,
                                                    [randrange(StartPeriodLow, StartPeriodHigh),
                                                     randrange(StartPeriodLow, StartPeriodHigh)],
                                                    node_index))

    @staticmethod
    def comp():
        for light in LightsController.traffic_lights:
            light.Change()


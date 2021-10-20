from random import randrange
from Util.TrafficLightInstance import TrafficLight
from Util.Consts import StartPeriodLow, StartPeriodHigh

class TrafficLightsController:

    traffic_lights : list[TrafficLight] = []

    @staticmethod
    def __init__(self):


        for node_index, node in enumerate(Map.nodes):
            self.traffic_lights.append(TrafficLight(node.end_nodes,
                                                    [randrange(StartPeriodLow, StartPeriodHigh),
                                                     randrange(StartPeriodLow, StartPeriodHigh)],
                                                    node_index))




from .NodeInstance import Node
from .MapController import Map
from.LineInstance import Line
from .RoadInstance import Road
from math import pi, cos, sin

class TrafficLight:
    # Lines, which connected to node, separated into two arrays:
    array_roads : list[list[Road], list[Road]] = [[], []]

    # Those arrays represent the separation for traffic light
    # We declare that traffic light has two periods
    periods : list[int, int]
    _is_first_open : bool = True
    counter : int = 0

    # When period one changes : traffic light 1 and 3 (2 and 4) change the colours to green (red)
    #                           traffic light 2 and 4 (1 and 3) change the colours to red (green)
    # For the another period : just vice versa
    #
    #           |   |
    #           |   |
    #           |(2)|
    # ======(3)=     =(1)=====
    #           |(4)|
    #           |   |
    #           |   |
    # /X-intersection by invalid art creator/
    #
    # For lines stopping implementation we will just change the last cell in lines
    # (for instance, line = [0, 0, 0, 1, 0, 0] -> [0, 0, 0, 1, 0, 1])


    def __init__(self, array_of_roads,  init_periods, index):
        # In the beginning, we used random function for distribution of lines

        # sample_roads1 = sample(array_of_roads, len(array_of_roads) // 2)
        # sample_roads2 = [array_of_roads[i] for i, road in enumerate(array_of_roads) if not (road in sample_roads1)]
        #
        # self.array_roads = [sample_roads1, sample_roads2]

        # Another application of setting the roads into types
        # We implemented the algorithm that used finding delta angles of roads
        # That means if delta angle of two roads is more than 3*pi/4 and less than 5*pi/4,
        # we will insert those roads into the first group
        # (for example, the first road has angle equals 1 radian and the second road has angle 4 radians,
        # their delta angle equals 3 radians which satisfied our condition)

        group1 = []
        group2 = []

        group1.append(array_of_roads[0])
        for road in array_of_roads[1:]:
            delta_angle = 4 * abs(road.angle - group1[0].angle)
            if delta_angle <= 5*pi and delta_angle >= 3*pi:
                group1.append(road)
            else:
                group2.append(road)

        self.array_roads = [group1, group2]


        # initializing the periods

        self.periods = init_periods
        self.node : Node = Map.nodes[index]
        self.center : int = Map.nodes[index].apos

    def ChangeLine(self):
        if self._is_first_open:
            for road in self.array_roads[0]:
                for line in road.lines[road.end_node]:
                    line.cells[-1] = 0
            for road in self.array_roads[1]:
                for line in road.lines[road.end_node]:
                    line.cells[-1] = 1
        else:
            for road in self.array_roads[1]:
                for line in road.lines[road.end_node]:
                    line.cells[-1] = 0
            for road in self.array_roads[0]:
                for line in road.lines[road.end_node]:
                    line.cells[-1] = 1


        self._is_first_open = not self._is_first_open

    def Change(self):
        self.counter += 1
        flag = int(self._is_first_open)
        if self.counter >= self.periods[flag]:
            self.counter = 0
            self.ChangeLine()


    def getAttributes(self):
        
        sublights = []

        for array_road in enumerate(self.array_roads):
            for road in array_road:
                sublight = []
                color = ['green', 'yellow', 'red']

                R = 15
                offset = 7
                x = self.center[0] + R*cos(road.angle + pi) 
                y = self.center[1] - R*sin(road.angle + pi)



        return [self.array_roads, self.periods, self._is_first_open, self.counter]


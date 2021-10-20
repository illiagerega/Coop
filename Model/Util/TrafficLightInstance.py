from .NodeInstance import Node
from .MapController import Map

class TrafficLight:
    # Lines, which connected to node, separated into two arrays:
    array_lines1 : list[Line] = []
    array_lines2 : list[Line] = []

    # Those arrays represent the separation for traffic light
    # We declare that traffic light has two periods
    periods : list[int, int]
    is_first_open : bool = True

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
        # in the beginning, I used random function for distribution of lines
        sample_roads1 = sample(array_of_roads, len(array_of_roads) // 2)
        sample_roads2 = [array_of_roads[i] for i, road in enumerate(array_of_roads) if array_of_roads.index(road) == -1]

        for road in sample_roads1:
            self.array_lines1.extend(road.lines[index])

        for road in sample_roads2:
            self.array_lines2.extend(road.lines[index])

        # initializing the periods

        self.periods = init_periods
        self.node : Node = Map.nodes[index]


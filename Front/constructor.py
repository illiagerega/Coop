import math

class Constructor:
    
    offset_x: int = 0
    offset_y: int = 0
    scale: int = 10
    nodes = None
    roads = None

    @staticmethod
    def min_map(data, index):
        off_min = math.inf

        for struct in data:
            off_min = min(struct[0][index], off_min)

        return off_min

    @staticmethod
    def setSystem(nodes, roads, reload=False):

        if(Constructor.nodes == None or reload):
            Constructor.nodes = nodes

        if(Constructor.roads == None or reload):
            Constructor.roads = roads
        
        Constructor.offset_x = Constructor.min_map(nodes, 0)
        Constructor.offset_y = Constructor.min_map(nodes, 1)   

    @staticmethod
    def constructCars(cars):
        html = ''

        for car in cars:
            car_key = next(iter(car))
            position = car[car_key][0]
            x = (position[0][0]) + (-1410 + 691.8) - Constructor.offset_x  #x
            y = (position[0][1]) + (-510 + 472) - Constructor.offset_y #y
            rotate = (position[1]) * 180 / math.pi #rotate

            road = car[car_key][1]
            iroad1 = road[0]  # === car.getRoad().index
            iroad2 = road[1]
            if iroad1 in Constructor.roads[iroad2]:
                x += 6 * math.cos(rotate * 180 / math.pi)
                y -= 6 * math.sin(rotate * 180 / math.pi)

                html += f'<div class="car_red" id="{car_key}" style="left: {x}px; top: {y}px; transform: rotate({rotate}deg);"> </div>'
            else:
                html += f'<div class="car_red" id="{car_key}" style="left: {x}px; top: {y}px; transform: rotate({rotate}deg);"> </div>'

        return html

    @staticmethod
    def constructNodes():
        html = ''

        for index, node in enumerate(Constructor.nodes):
            x = (node[0][0] - Constructor.offset_x) * Constructor.scale
            y = (node[0][1] - Constructor.offset_y) * Constructor.scale
            node[0][0] = x
            node[0][1] = y

            html += f'<div class="main_circle" id="{index}" style="left: {x}px; top: {y}px;"></div>'

        return html

    @staticmethod
    def constructRoads():
        html = ''

        for iroad1 in Constructor.roads.keys():
            for iroad2 in Constructor.roads[iroad1].keys():
                if len(Constructor.roads[iroad1][iroad2]) == 0: 
                    continue
                
                x1 = Constructor.nodes[int(iroad1)][0][0] + 18
                y1 = Constructor.nodes[int(iroad1)][0][1] + 18
                x2 = Constructor.nodes[int(iroad2)][0][0] + 18
                y2 = Constructor.nodes[int(iroad2)][0][1] + 18

                x = (x1 + x2) / 2
                y = (y1 + y2) / 2

                length = ((abs(x1 - x2) ** 2) + (abs(y1 - y2) ** 2)) ** 0.5

                if iroad1 in Constructor.roads[iroad2]:
                    html += f'<div class="road" style="left: {(x - (length / 2))}px; top: {(y - 12)}px; width: {length}px; transform: rotate({Constructor.roads[iroad1][iroad2][1] * 180 / math.pi}deg);"></div>'
                else:
                    html += f'<div class="road_one_line" style="left: {(x - (length / 2))}px; top: {(y - 6)}px; width: {length}px; transform: rotate({Constructor.roads[iroad1][iroad2][1] * 180 / math.pi}deg);"></div>'

        return html
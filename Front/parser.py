import rabbitmq
import json
import math
from ast import literal_eval

offset_x = 0 
offset_y = 0
scale = 10


def min_map(data, index):
    off_min = math.inf

    for struct in data:
        off_min = min(struct[0][index], off_min)

    return off_min

def data():
    global offset_x, offset_y
    message = rabbitmq.receive('cars')

    if str(message).startswith("b'"):
        
        abc = str(message).replace("'", "").replace('b', '')

        data = json.loads(abc)
        # print(abc)

        html = ''

        # offset_x = min_cars(data['cars'], 0)
        # offset_y = min_cars(data['cars'], 1)

        # print(offset_x)
        #print(data['cars'])
        cars = data["cars"]
        # print(cars)        
        for car in cars:
            car_key = next(iter(car))
            x = ((car[car_key][0][0]) - offset_x + 1.8) * scale  #x
            y = ((car[car_key][0][1]) - offset_y + 2) * scale #y
            rotate = (car[car_key][1]) * 180 / math.pi #rotate

            html += f'<div class="car_red" id="{car_key}" style="left: {x}px; top: {y}px; transform: rotate({rotate}deg);"> </div>'

        

        return html
    else:
        return ''

def datamap():
    #message = rabbitmq.receive('map')
    global offset_x, offset_y

    message = '''{"nodes": [[[0, 0], "spawn"], [[-372, 118], "spawn"], [[-727, 221], "spawn"], [[-176, -24], "spawn"], [[-455, -15], "spawn"], [[-473, -10], "spawn"], [[-424, 35], "spawn"], [[-439, 39], "spawn"], [[-413, 53], "spawn"], [[-394, 47], "spawn"], [[-374, 114], "spawn"], [[-473, 53], "spawn"], [[-444, 40], "spawn"], [[-379, 121], "spawn"], [[-382, 117], "spawn"], [[-333, 177], "spawn"], [[-339, 28], "spawn"], [[-287, 94], "spawn"], [[-306, 71], "spawn"], [[-187, 28], "spawn"]], "roads": {"0": {"17": [1, -0.3165150001402346]}, "1": {"13": [1, -0.4048917862850834], "10": [1, 1.1071487177940906], "15": [1, 0.9867152717720891], "17": [1, -0.2751892491291713]}, "2": {"13": [1, -0.27981710852324315]}, "3": {"16": [1, -0.3088122745486295]}, "4": {"6": [1, 1.0158005994563097]}, "5": {"7": [1, 0.9641912182003697]}, "6": {"7": [1, -0.26060239174734096], "8": [1, 1.0222469243443686], "4": [1, 1.0158005994563097]}, "7": {"6": [1, -0.26060239174734096], "12": [1, -0.19739555984988078], "14": [1, 0.9397169393235674], "5": [1, 0.9641912182003697]}, "8": {"10": [1, 1.0019484683735376], "9": [1, -0.30587887140485215], "6": [1, 1.0222469243443686]}, "9": {"8": [1, -0.30587887140485215], "16": [1, -0.33261969157391236]}, "10": {"1": [1, 1.1071487177940906], "8": [1, 1.0019484683735376]}, "11": {"12": [1, -0.4214192068878042]}, "12": {"7": [1, -0.19739555984988078], "11": [1, -0.4214192068878042]}, "13": {"1": [1, -0.4048917862850834], "14": [1, 0.9272952180016122], "2": [1, -0.27981710852324315]}, "14": {"13": [1, 0.9272952180016122], "7": [1, 0.9397169393235674]}, "15": {"1": [1, 0.9867152717720891]}, "16": {"9": [1, -0.33261969157391236], "18": [1, 0.9162255594715053], "3": [1, -0.3088122745486295]}, "17": {"18": [1, 0.8803498697402046], "1": [1, -0.2751892491291713], "0": [1, -0.3165150001402346]}, "18": {"17": [1, 0.8803498697402046], "16": [1, 0.9162255594715053], "19": [1, -0.34674534801556234]}, "19": {"18": [1, -0.34674534801556234]}}}'''
    if message.startswith('{"nodes":'):
        abc = str(message).replace("'", "").replace('b', '')

        data = json.loads(abc)

        html = ''
        # count = 0

        nodes = literal_eval(str(data['nodes']))
        roads = literal_eval(str(data['roads']))

        offset_x = min_map(nodes, 0)
        offset_y = min_map(nodes, 1)

        for index, node in enumerate(nodes):
            x = (node[0][0] - offset_x) * scale
            y = (node[0][1] - offset_y) * scale
            node[0][0] = x
            node[0][1] = y

            html += f'<div class="main_circle" id="{index}" style="left: {x}px; top: {y}px;"></div>'
        
       #  print(roads)

        for iroad1 in roads.keys():
            for iroad2 in roads[iroad1].keys():
                if len(roads[iroad1][iroad2]) == 0: 
                    continue
                
                x1 = nodes[int(iroad1)][0][0] + 18
                y1 = nodes[int(iroad1)][0][1] + 18
                x2 = nodes[int(iroad2)][0][0] + 18
                y2 = nodes[int(iroad2)][0][1] + 18

                x = (x1 + x2) / 2
                y = (y1 + y2) / 2

                length = ((abs(x1 - x2) ** 2) + (abs(y1 - y2) ** 2)) ** 0.5

                if iroad1 in roads[iroad2]:
                    html += f'<div class="road" style="left: {(x - (length / 2))}px; top: {(y - 12)}px; width: {length}px; transform: rotate({roads[iroad1][iroad2][1] * 180 / math.pi}deg);"></div>'
                else:
                    html += f'<div class="road_one_line" style="left: {(x - (length / 2))}px; top: {(y - 6)}px; width: {length}px; transform: rotate({roads[iroad1][iroad2][1] * 180 / math.pi}deg);"></div>'





        return html
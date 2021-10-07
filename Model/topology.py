#  nodes = [Id1, Id2, ...]
#  roads = [Id1, Id2, ...]
#  Set nodes() :
#
#
import model
import transport

def GetDistances(nodes):
    dmat = []
    for node in nodes:
        mat = [[0, None]]*len(nodes)
        for i in node.start_roads:
            mat[i.end_node] = [i.length, i]
        dmat.append(mat)

    return dmat



class Topology:
    def __init__(self, nodes, roads, n_cars, spawn_nodes):
        self.nodes = nodes
        self.roads = roads

        self.car_driver = transport.CarDriver(nodes, roads, n_cars, spawn_nodes, GetDistances(self.nodes))

    def Comp(self):
        self.car_driver.Comp()


topology = None

if __name__ == '__main__':
    n_nodes, n_roads, n_cars = list(map(int, input().split()))
    nodes = {}
    spawn_nodes = []
    roads = {}

    for i in range(n_nodes):
        type, x, y = list(map(int, input().split())) # types: 0 - spawn, 1 - intersect
        node = model.Node(type, (x, y))
        nodes[i] = node

        if type == 0:
            spawn_nodes.append(i)

    for i in range(n_roads):
        s_n, e_n, n_lines = list(map(int, input().split())) # start node, end node, length, number of lines, absolute position
        road = model.Road(s_n, e_n, n_lines)
        roads[i] = road

        nodes[s_n].addRoad(road)
        nodes[e_n].addRoad(road, 'end')

        if n_lines > 1:
            nodes[e_n].addRoad(road)
            nodes[s_n].addRoad(road, 'end')

    # spawn_point, end_point = list(map(int, input().split()))

    #way = list(map(int, input().split()))

    topology = Topology(nodes, roads, n_cars, spawn_nodes)

    print(nodes)
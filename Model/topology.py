#  nodes = [Id1, Id2, ...]
#  roads = [Id1, Id2, ...]
#  Set nodes() :
#
#
import transport
import dijkstra

def GetDistances(nodes):
    dmat = []
    k = 0
    for node in nodes:
        mat = [[0, None]]*len(nodes)
        for i in node.start_roads:
            if i.end_node != k:
                mat[i.end_node] = [i.length, i]
            elif i.start_node != k and i.lines != 1:
                mat[i.start_node] = [i.length, i]
            else:
                pass

        dmat.append(mat)
        k += 1

    return dmat



class Topology:
    def __init__(self, nodes, roads, n_cars, spawn_nodes):
        self.nodes = nodes
        self.roads = roads
        self.dmat = GetDistances(self.nodes)
        self.car_driver = transport.CarDriver(nodes, roads, n_cars, spawn_nodes, self.dmat)

    def Comp(self):
        self.car_driver.Comp()

    def GetPath(self, u, v):
        return dijkstra.find_shortest_path(self.dmat, u, v)
import topology
import model


graph = open("test.txt", 'r')


opology = None
n_nodes, n_roads, n_cars = list(map(int, graph.readline().split()))
nodes = [None]*n_nodes
spawn_nodes = []
roads = [None]*n_roads

for i in range(n_nodes):
    type, x, y = list(map(int, graph.readline().split())) # types: 0 - spawn, 1 - intersect
    node = model.Node(type, (x, y))
    nodes[i] = node

    if type == 0:
        spawn_nodes.append(i)

for i in range(n_roads):
    s_n, e_n, n_lines = list(map(int, graph.readline().split())) # start node, end node, length, number of lines, absolute position
    road = model.Road(nodes, s_n, e_n, n_lines)
    roads[i] = road

    nodes[s_n].addRoad(road)
    nodes[e_n].addRoad(road, 'end')

    if n_lines > 1:
        nodes[e_n].addRoad(road)
        nodes[s_n].addRoad(road, 'end')

# spawn_point, end_point = list(map(int, input().split()))

#way = list(map(int, input().split()))

opology = topology.Topology(nodes, roads, n_cars, spawn_nodes)

with open("output.txt", 'w') as f:
    for mat in opology.GetPath(0, 2):
        for at in mat:
            f.write(str(at))

        #f.write('\n')



print(nodes)
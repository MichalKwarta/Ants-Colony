from Nodes import  NodesList

FILENAME = "data/berlin52.txt"


# points = PointsList(FILENAME)
# path, _ = points.Ants(plot=True)
nodes = NodesList()
nodes.readNodes("data/test5.txt")
path, distance = nodes.Ants(plot=True)
print(distance)
path,distance = nodes.greedy(plot=True)
print(distance)
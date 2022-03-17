from Nodes import NodesList

FILENAME = "data/test8.txt"


# points = PointsList(FILENAME)
# path, _ = points.Ants(plot=True)
nodes = NodesList(FILENAME)
path, distance = nodes.greedy(plot=True)
print(distance)

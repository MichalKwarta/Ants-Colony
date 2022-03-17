from Nodes import NodesList

FILENAME = "data/berlin52.txt"


# points = PointsList(FILENAME)
# path, _ = points.Ants(plot=True)
nodes = NodesList()

path, distance = nodes.greedy(plot=True)
print(distance)

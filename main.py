

from point import  PointsList

FILENAME = "data/berlin52.txt"


points = PointsList(FILENAME)

path, _ = points.Ants(plot=True)

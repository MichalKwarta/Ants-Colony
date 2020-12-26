from point import *
from drawing import draw

l=Point.read('berlin52.txt')
greedy=Point.greedy(l)
ants=Point.Ants(l)
print("greedy: ",greedy[1])
print("Ants: ",ants[1])





from point import *
from drawing import draw

l=Point.read('berlin52.txt')
#greedy=Point.greedy(l)
for k in range(10):
    ants=Point.Ants(l,0.2, 3, 7, 40, 10)
    #print("greedy: ",greedy[1])
    print("Ants: ",ants[-1])





from point import *
from random import randint 
l1=[generatelistofinstances(10*randint(1,50)) for k in range(15)]


l2=[[(p.id,p.x,p.y) for p in l] for l in l1]

l3=list(zip(l1,l2))
for points,cords in l3:
    print(str(Point.greedy(points)[-1]).replace('.',','),str(Point.Ants(cords,0.2,6,61,30)[-1]).replace('.',','),sep='\t')

from point import * 
from drawing import *
l=Point.read("Ants_testing_data.txt")
#rysowanie iteracji 1,5,10
# out=Point.Ants_testing(l,0.1,5,1,30)
# print(out,sep='\n')

# draw(list_to_point(l,out[0][0]))
# draw(list_to_point(l,out[4][0]))
# draw(list_to_point(l,out[-1][0]))

l=Point.read("data/tsp250.txt")
print(Point.Ants(l))
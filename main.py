from point import *
from drawing import draw
from os import listdir,getcwd
from time import time
start=time()

files=[f[:-4] for f in listdir(getcwd()+"/data")]
distances_Ants={instance:
Point.Ants(
Point.read(getcwd()+"\\data\\"+instance+'.txt'),0.2, 6, 61, 30)[-1] 
for instance in 
files}

ACO_TIME=time()-start
start=time()

distances_Greedy = {instance:Point.greedy(Point.readPoints(getcwd()+"\\data\\"+instance+'.txt'))[-1] for instance in files}

GREEDY_TIME=time()-start
print("nazwa instancji\twynik")
print("ACO")

for name,dist in distances_Ants.items():
    print(f"{name}  {round(dist,2)}")

print("GREEDY")
for name,dist in distances_Greedy.items():
    print(f"{name}  {round(dist,2)}")
print(f"ACO liczyło {round(ACO_TIME)}s\t GREEDY liczył {round(GREEDY_TIME)}s")




from point import *
from drawing import draw
from os import listdir,getcwd
from time import time,localtime,strftime

eva,alpha,beta,ants=0.2, 15, 200,30
eva,alpha,beta,ants=0.15,9,12,30
eva,alpha,beta,ants=0.2,5,3,30
eva,alpha,beta,ants= 0.2,6,61,30
start=time()

files=[f[:-4] for f in listdir(getcwd()+"/data")]


distances_Ants={instance:
Point.Ants(
l:=Point.read(getcwd()+"\\data\\"+instance+'.txt'),eva,alpha,beta,30)
for instance in 
files}

ACO_TIME=time()-start
start=time()

distances_Greedy = {instance:Point.greedy(Point.readPoints(getcwd()+"\\data\\"+instance+'.txt'))[-1] for instance in files}

GREEDY_TIME=time()-start
print("\anazwa instancji\twynik\tczas testu: ",pomiar:=strftime("%H:%M",localtime()))
print("ACO")
#berlin działa super dla eva,alpha,beta,ants=0.2,5,3,30
#wstepnie optymalne parametry = 0.2,6,61,30
for name,dist in distances_Ants.items():
    print(f"{name}  {round(dist[1],2)}")

# print("GREEDY")
# for name,dist in distances_Greedy.items():
#     print(f"{name}  {round(dist,2)}")
print(f"ACO liczyło {round(ACO_TIME)}s\t GREEDY liczył {round(GREEDY_TIME)}s")

paramslist=[eva,alpha,beta,ants]
fname=str(paramslist)[1:-1].replace(',','_')+'_'+pomiar.replace(':','_')+'.txt'
with open(fname,'w') as f:
    for name,comb in distances_Ants.items():
        print(name,comb[0],file=f)
    for name,comb in distances_Ants.items():
        print(name,comb[1],file=f)



    
import point
import file
listofinstances=file.read("asd.txt")
#listofinstances=point.generatelistofinstances(10)
#file.write('out.txt',listofinstances)
print(*listofinstances,sep='\n')
print()
matrix=point.generatematrix(listofinstances)
start=listofinstances[0]
path=[listofinstances[0]]
listofinstances=listofinstances[1::]
distance=0
while listofinstances!=[]:
    next,delta=path[-1].getclosest(listofinstances)
    distance+=delta
    path.append(next)
    listofinstances.pop(listofinstances.index(next))
print(*path,sep='\n')
print(f"distance: {distance}")
#print(*matrix,sep='\n')
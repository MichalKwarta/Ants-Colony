import point
import file
listofinstances=file.read("out.txt")
#listofinstances=point.generatelistofinstances(10)
#file.write('out.txt',listofinstances)
print(*listofinstances,sep='\n')
print()
matrix=point.generatematrix(listofinstances)
start=listofinstances[0]
path=[listofinstances[0]]
listofinstances=listofinstances[1::]

while listofinstances!=[]:
    next=path[-1].getclosest(listofinstances)
    path.append(next)
    listofinstances.pop(listofinstances.index(next))
print(*path,sep='\n')

print(*matrix,sep='\n')
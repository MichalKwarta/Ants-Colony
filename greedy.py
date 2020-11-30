import point
import file


def greedy(listofinstances):
    path=[listofinstances[0]] #biore pierwszy wierzcholek jako poczatek

    listofinstances=listofinstances[1::] 
    distance=0

    while listofinstances!=[]:
        next,delta=path[-1].getclosest(listofinstances) 
        distance+=delta
        path.append(next)
        listofinstances.pop(listofinstances.index(next))

    distance+=path[0].getdistance(path[-1]) #zamykam cykl 
    path.append(path[0])
    return path,distance


# for num in range(1,4):
#     listofinstances=point.generatelistofinstances(50)

#     file.write('in'+str(num)+'.txt',listofinstances)
#     path,distance=greedy(listofinstances)
#     file.write('out'+str(num)+'.txt',path,distance)
    
#     listofinstances.clear()
#     path.clear()

    


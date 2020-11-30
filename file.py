import point
from point import Point
def write(filename,list,distance=None):
    f=open(filename,'w+')
    print(point.Point.count,file=f)
    for object in list:
        print(object,file=f)
    print(distance,file=f)

def read(filename):
    f=open(filename,'r')
    count=int(f.readline())
    l=f.readlines()
    if len(l)!=count:
        raise('błąd danych')
    obj_list=[]
    for el in l:
        a,b,c=map(int,el[:-1].split())
        obj_list.append(point.Point(a,b,c))
        
    return obj_list
#print(*read('data.txt'),sep='\n')
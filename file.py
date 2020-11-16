import point
from point import Point
def write(filename,list):
    f=open(filename,'w+')
    print(point.Point.count)
    for object in list:
        print(object,file=f)

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
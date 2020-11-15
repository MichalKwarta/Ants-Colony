import point
from point import Point
def write(filename,list):
    f=open(filename,'w+')
    for object in list:
        print(object,file=f)

def read(filename):
    f=open(filename,'r')
    l=f.readlines()
    obj_list=[]
    for el in l:
        a,b,c=map(int,el[:-1].split())
        obj_list.append(point.Point(a,b,c))
        print(a,b,c)
    return obj_list

# print(*read('test.txt'),sep='\n')
# print()
# print(Point.random(),Point.random())
from random import randint
MAX=50

class Point:
    count=0
    cords=[]   #check if coordinates were already used 
    def __init__(self,id,X,Y):
        Point.count+=1
        self.id=id
        if (X,Y) in Point.cords:
            raise("Już jest taki punkt")
        Point.cords.append((X,Y))
        self.x=X
        self.y=Y
        
    def __del__(self):
        Point.count-=1
        Point.cords.remove((self.x,self.y))


    @classmethod
    def random(cls):
        X,Y=randint(0,MAX),randint(0,MAX)
        while (X,Y) in Point.cords:
            X,Y=randint(0,MAX),randint(0,MAX)
        return cls(Point.count+1,X,Y)

  
    def getdistance(self,p2):
        return ((self.x-p2.x)**2+(self.y-p2.y)**2)**0.5

    def getclosest(self,l:list): # zakładam, że nie znajduje sie na liście
        closest=l[0]
        delta_distance=self.getdistance(closest)
        for point in l[1::]:
            if self.getdistance(point)<self.getdistance(closest):
                closest=point
                delta_distance=self.getdistance(closest)
        return closest,delta_distance

    def __str__(self):
        return f"{self.id} {self.x} {self.y}"

def generatelistofinstances(n:int):
    l=[]
    for k in range(n):
       l.append(Point.random())
    return l  

def generatematrix(l:list):
    matrix=[]
    for p1 in l:
        row=[]
        for p2 in l:
            if p2==p1:
                row.append(-1)
            else:
                row.append(round(p1.getdistance(p2))) #FIXME: TO TYLKO POGLĄDOWE BO JEST ZAOKRĄGLANIE
        matrix.append(row)
    return matrix 

                



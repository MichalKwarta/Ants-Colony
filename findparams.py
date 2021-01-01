from point import *
from multiprocessing import Pool,freeze_support
from time import sleep
def main():
    l=Point.read("berlin52.txt")
    solutions=[]
    total_iterations=36000 #4 petle
    curr=0
    for eva in range(1,11): 
        for alpha in range(1,100,5):
            for beta in range(1,100,5): 
                for count in range(100,501,50): 
                    curr+=1
                    args=[(l,eva/10,alpha,beta,count,it) for it in range(20,101,5)]
                    with Pool(3) as pool: #w Pool wstawiasz liczbe wątków ile chcesz użyć, Ty masz 8 w procku
                        results=pool.starmap(Point.Ants,args)
                    for el in results:
                        solutions.append(el)
                    print(f"progress = {(curr/total_iterations)*100} %")

    
    f=open("params.txt",'w')
    solutions.sort(key=lambda x: x[-1])
    for el in solutions:
        print(el,file=f)

if __name__=="__main__":
    freeze_support()
    t=main()
    print("koniec main")
    

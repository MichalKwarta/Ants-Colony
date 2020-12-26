from point import *
from multiprocessing import Pool,freeze_support
def main():
    l=Point.read("berlin52.txt")
    solutions=[]
    total=1
    for eva in range(1,11): #11
        for alpha in range(1,100,5):
            for beta in range(1,100,5):
                for count in range(10,501,50):
                        args=[(l,eva/10,alpha,beta,count,it) for it in range(5,100,5)]
                        print(args[1:])
                        total+=3
                        print(eva/10,alpha,beta,count)
                        with Pool(3) as pool:
                            results=pool.starmap(Point.Ants,args)
                        for el in results:
                            solutions.append(el)

    print(solutions)
    f=open("params.txt",'w')
    solutions.sort(key=lambda x: x[-1])
    for el in solutions:
        print(el,file=f)

if __name__=="__main__":
    freeze_support()
    t=main()
    print("koniec main")
    
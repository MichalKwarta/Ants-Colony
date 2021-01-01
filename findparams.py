from point import *
from multiprocessing import Pool,freeze_support
from time import sleep,time
def main():
    l=Point.read("berlin52.txt")
    solutions=[]
    total_iterations=4000 #4 petle
    curr=0
    f=open("tmpdatastorage.txt","w")
    for eva in range(1,11): #10
        for alpha in range(1,101,5): #20
                    start=time()
                    args=[(l,eva/10,alpha,beta,400,40) for beta in range(1,101,5)] #20 
                    '''
                    TODO: Dopasuj 2 ostatnie parametry - ilosc mrówek i iteracji(400,40)
                    tak żeby były dość duże ale nie mieliło za długo, wiesz o co chodzi xD
                    bo tego po prostu im wiecej tym lepiej raczej
                    najwazniejsze zeby dobrac evaporation alphe i bete
                    '''

                    with Pool(3) as pool: #w Pool wstawiasz liczbe wątków ile chcesz użyć, Ty masz 8 w procku
                        results=pool.starmap(Point.Ants,args)
                    for el in results:
                        solutions.append(el)
                        print(el,file=f) #pisanie do pliku tymczasowego
                    end=time()-start
                    curr+=20 # beta ma 20 iteracji
                    print(f"progress= {round(((curr/total_iterations)*100),3)}%, pętla nr {curr} zajęła {round(end,2)} sekund")

    #jeśli nic sie nie stanie po drodze to ten plik bedzie posortowany
    f=open("params.txt",'w')
    solutions.sort(key=lambda x: x[-1])
    for el in solutions:
        print(el,file=f)

if __name__=="__main__":
    freeze_support()
    t=main()
    print("koniec main")
    

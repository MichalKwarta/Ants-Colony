from matplotlib import pyplot as plt
import file 
import point



def drawArrow(A, B,head): #punkt punkt szerokosc_zakonczenia
    plt.arrow(A[0], A[1], B[0] - A[0], B[1] - A[1],
              head_width=head, length_includes_head=True,color='r',linestyle='-')

def draw(l:list):
    #l=list of instances
    print(*l,sep='\n')

    plt.plot([p.x for p in l],[p.y for p in l],'bo')

    for i in range(len(l)-1):
        drawArrow((l[i].x,l[i].y),(l[i+1].x,l[i+1].y),1+0.01*len(l))

    drawArrow((l[-1].x,l[-1].y),(l[0].x,l[0].y),1+0.01*len(l))
    for p in l:
        plt.annotate(p.id,(p.x,p.y))

    plt.show()


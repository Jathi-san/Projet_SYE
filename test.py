# on importe notre fichier biblio qui comporte toutes nos fonctions
from biblio import *

# on importe aussi memory pour simuler la manipulation de cases memoires par les taches
import memory


# on defini ici des fonctions qui vont etre effectue par la tache qui vont l'appeler :

def runT1():

    #on declare les cases memoires que la fonction (tache) va utiliser
    memory.V, memory.W, memory.X
    
    # l'ajout de sleep permet de mieux visualiser les temps d'execution entre sequentielle et parallele 
    time.sleep(1)

    # on declare l'action effectue (lit dans V et W puis met la somme de ces valeurs dans X)       
    memory.X = memory.V+memory.W

# meme principe pour toutes les autre fonctions :
    
def runT2():
    memory.V, memory.Y
    time.sleep(1)
    memory.Y = memory.V

def runT3():
    memory.V, memory.X, memory.Y
    time.sleep(1)
    memory.V = memory.X*memory.Y

def runT4():
    memory.X, memory.Y, memory.Z
    time.sleep(1)
    memory.Z = memory.Y-memory.X

def runT5():
    memory.W, memory.Y
    time.sleep(1)
    memory.W = memory.Y

def runT6():
    memory.Z
    time.sleep(1)
    memory.Z = memory.Z

def runT7():
    memory.V, memory.W, memory.Y
    time.sleep(1)
    memory.Y = memory.V+memory.W+memory.Y

def runT8():
    memory.V, memory.X, memory.Z
    time.sleep(1)
    memory.Z = memory.X-memory.V

def runT9():
    memory.A
    time.sleep(1)
    memory.A = 1

def runT10():
    memory.B
    time.sleep(1)
    memory.B = 2

def runTS():
    memory.A, memory.B, memory.C
    memory.C = memory.A + memory.B

# on declare ici toutes nos taches :

t1 = Task("T1",reads=["V","W"],writes=["X"],run=runT1)
t2 = Task("T2",reads=["V"],writes=["Y"],run=runT2)
t3 = Task("T3",reads=["X","Y"],writes=["V"],run=runT3)
t4 = Task("T4",reads=["X","Y"],writes=["Z"],run=runT4)
t5 = Task("T5",reads=["Y"],writes=["W"],run=runT5)
t6 = Task("T6",reads=["Z"],writes=["Z"],run=runT6)
t7 = Task("T7",reads=["V","W","Y"],writes=["Y"],run=runT7)
t8 = Task("T8",reads=["V","X"],writes=["Z"],run=runT8)
t9 = Task("T9",reads=[],writes=["A"],run=runT9)
t10 = Task("T10",reads=[],writes=["B"],run=runT10)
tS = Task("TS",reads=["A","B"],writes=["C"],run=runTS)

# on declare ici les systemes de taches :

s1 = SeTask([t9, t10, tS], {"T9": [],"TS": ["T10","T9"], "T10": ["T9"] })
s2=SeTask([t4,t5,t3,t6,t2,t1,t8,t7],{"T2":["T1"],"T3":["T2"],"T4":["T2"],"T5":["T3","T4"],"T6":["T4"],"T7":["T5","T6"],"T8":["T7"]})
s3 = SeTask([t9, t10, tS], {"T9": ["TS"],"TS": ["T10","T9"], "T10": ["T9"] })
s4=SeTask([t4,t5,t3,t6,t2,t1,t8,t7],{"T2":["T9"],"T3":["T2"],"T4":["T2"],"T5":["T3","T4"],"T6":["T4"],"T7":["T5","T6"],"T8":["T7"]})
s5=SeTask([t4,t5,t3,t6,t2,t1,t8,t7],{"T9":["T1"],"T3":["T2"],"T4":["T2"],"T5":["T3","T4"],"T6":["T4"],"T7":["T5","T6"],"T8":["T7"]})
s6 = SeTask([t2, t7], {"T2": []})
s7 = SeTask([t2], {"T2": []})

# on teste nos fonction du systeme de taches 

#s3.Erreur()
#s4.Erreur()
#s5.Erreur()
#s6.Erreur()
#s7.Erreur()

#print(s1.getDependenciesSeq("T3"))
#print(s2.getDependenciesSeq("T7"))
#print(s5.getDependenciesSeq("T5"))

#print(s3.getTaskByName("TS").name)
#print(s3.getTaskByName("T5"))

#s1.drawSeq()
#s2.drawSeq()

#s1.runSeq()
#s2.runSeq()

#print(s2.getDependencies("T7"))

# for l in s2.interference():
    #print(l)

#s1.run()
#s2.run()

#s1.draw()
#s2.draw()

#s1.detTestRnd(2)
#s2.detTestRnd(2)

#s1.parCost(2)
#s2.parCost(2)

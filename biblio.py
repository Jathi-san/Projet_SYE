# pour mieux visualiser le code :

# ----------- les blocs entre ce type de ligne seront des classes -----------
# *********** les blocs entre ce type de ligne seront des fonctions de la classe ***********
# ''''''''''' les blocs entre ce type de ligne seront des sous fonction de ces fonctions '''''''''''
# ^^^^^^^^^^^ les blocs entre ce type de ligne seront des sous fonction de ces sous fonctions ^^^^^^^^^^^
# ........... sous fonction du bloc plus haut ...........


# importation des differents modules :

# pour affichage de la page
import matplotlib.pyplot as mp

# pour créer le graphe
import networkx as nt

# on va utiliser NetworkXNoCycle pour savoir si un graphe na pas de cycle
from networkx.exception import NetworkXNoCycle

import time
import threading
import random

# on importe aussi memory pour mettre par la suite des valeurs aleatoires dans nos cases memoire (por detTestRnd())
import memory 




# definition de la classe task
    # premier argument : nom de la tache
    # deuxieme arguments : domaine de lecture de la tache sous forme de liste
    # troisieme argument : domaine d'ecriture de la tache sous forme de liste
    # quatrieme argument la fonction que la tache va executer

#-----------------------------------------------------------------------------------------------------------------
class Task:

    #**************************************************************************************************************
    def __init__(self,name,reads=[],writes=[],run=None):
        self.name = name
        self.reads = reads
        self.writes = writes
        self.run = run

        # ce statut va nous servir lors de l'execution sequentielle, il passera a vrai lorsque la tache sera execute
        self.state= False 

        # lorsque l'on declare nos taches dans le systeme de tache, elles ne sont pas forcement
        # dans l'ordre dans lequel elles vont s'executer, donc par defaut on considere
        # que la tache n'est pas dans le bon ordre, on va la mettre dans le bon ordre lors
        # de la construction du systeme de paralelisme maximal
        self.ordered = False
    #**************************************************************************************************************
#-----------------------------------------------------------------------------------------------------------------



# definition de la classe de systeme de tache

#-----------------------------------------------------------------------------------------------------------------   
class SeTask:

    # construction du systeme de tache
        # premier argument : liste des taches du systeme (pas forcement dans l'ordre d'execution)
        # deuxieme argument dictionnaire de precedence :
            # il se presente sous la forme d'un ensemble cle valeur avec la cle qui est le nom de la tache
            # et la valeur qui correspond à une liste de taches dont depend la tache qui est represente par la cle
        # on definit aussi les attributs suivants :
            # self.ordered_tasks = [] corespondant a une liste des taches du systeme dans l'ordre
                # dans lesquelles elles vont s'executer
            # self.G correspondant au graphe oriente tel qu'il nous est decrit dans le dictionnaire de precedence
            # self.precedence_dico_paral = {} corespondant (quand c'est possible) 
                # au dictionnaire de precedence du systeme lorsqu'il est paralelise au maximum 

    #**************************************************************************************************************
    def __init__(self, tasks=[], precedence_dico={}):
        self.tasks = tasks
        self.precedence_dico = precedence_dico
        self.ordered_tasks = []

        # G est un graphe oriente
        self.G= nt.DiGraph()

        # pour chaque tache du systeme
        for task in self.tasks:

            #on ajoute un sommet au graphe
            self.G.add_node(task.name)

            for dep in self.getDependenciesSeq(task.name):

                # pour chaque dependances de cette tache on ajoute un arc qui va de cette dependance a la tache
                self.G.add_edge(dep,task.name)

        self.precedence_dico_paral = {}
    #**************************************************************************************************************


    # le systeme de tache a aussi plusieurs fonctions:
        # Erreur()                    ligne 117
        # getTaskByName()             ligne 345
        # getDependenciesSeq()        ligne 364
        # drawSeq()                   ligne 377 
        # runSeq()                    ligne 390
        # interference()              ligne 469
        # getDependencies()           ligne 615
        # run()                       ligne 662
        # draw()                      ligne 826
        # detTestRnd()                ligne 846
        # parCost()                   ligne 933


    # verifie si un systeme de tache est correctement definit
    # effectue les verifications suivante :
        # si le systeme a au moins 2 taches
        # si il n'y a pas de doublons
        # si dans le dictionnaire de precendences les taches sont bien des taches connus (qui appartiennent au systeme)
        # si le systeme en question est deterministe
        # si les taches ne s'attendent pas mutuellement 
    #**************************************************************************************************************
    def Erreur(self):

        # pour effectuer ces verifications on aura besoin de plusieurs fonctions:
            # getKey()                ligne 129
            # bernstein()             ligne 137
            # isCyclic()              ligne 271

        
        # renvoie les cles (taches) inscrit dans le dictionnaire de precedence
        # voir fonction Erreur() pour connaitre son utilite

        #'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        def getKey():
            return self.precedence_dico.keys()
        #'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


        # verifie les conditions de Bernstein pour savoir si un systeme est deterministe

        #'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        def bernstein():

            # on veut trouver les couples de sommets qui n'ont pas de chemin entre eux
            # mais le probleme que l'on va rencontrer c'est que si l'on a un graphe oriente 
            # il peut ne pas y avoir de chemin entre deux sommets dans un sens mais  
            # il peut y avoir un chemin dans l'autre sens c'est pourquoi on verifie que pour chaque couple, 
            # il n'y a pas de chemins qui existe entre le sommet 2 et 1 on sait qu'il n'y en a pas 
            # entre le sommet 1 et 2 grace a la fonction find_disconnected_pairs decrite ci dessous
            # et donc cette fonction diconnected_pairs va nous renvoyer la liste des couples de sommet 
            # qui n'ont pas de chemin peu importe le sens 

            #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
            def diconnected_pairs():

                # afin de verifier les condition de Bernstein il nous faut d'abord connaitre
                # les taches qui n'ont pas de relations de precedence entre elles 
                # cette fonction va pour un graphe de syteme, renvoyer les paires de taches qui ne sont pas connecte
                # (pas de chemin entre elles)

                #......................................................................................................
                def find_disconnected_pairs(graph):   

                    # on declare une liste qui contiendra les pairs
                    disconnected_pairs = []  

                    # on parcourt les sommets du graphe 
                    for node1 in graph.nodes:

                        # on utilise la fonction single_source_shortest_path pour calculer les chemins les plus courts
                        # a partir du sommet node1 vers tous les autres sommets
                        visited = set(nt.single_source_shortest_path(graph, node1))

                        # parcourt les sommets du graphe
                        for node2 in graph.nodes:

                            # on declare une liste qui contiendra les 2 sommets deconnecte (si ils le sont)
                            couple = []

                            # et justement si node2 n'est pas dans visited c'est que de node1 il n'y a pas de plus court chemin
                            # voir pas de chemin du tout et donc node1 et node2 sont deconnecte
                            if node1 != node2 and node2 not in visited:

                                # on ajoute node1 et node2 dans couple
                                couple.append(node1)
                                couple.append(node2)

                                # puis on ajoute couple dans la liste des pairs de sommet deconnecte
                                disconnected_pairs.append(couple)

                    # enfin on retourne la liste de pairs de sommet deconnecte
                    return disconnected_pairs
                #......................................................................................................

                # une fois la fonction find_disconnected_pairs definit
                # on declare une liste qui contiendra les pairs
                disconnected_pairs = []

                # on parcourt les couples de sommets qui ne sont pas censé etre connecte
                for couple in find_disconnected_pairs(self.G):

                    # et on verifie qu'il n'y a pas de chemin entre le sommet 2 (couple[1] et le sommet 1 (couple[0]))
                    if nt.has_path(self.G, couple[1], couple[0])==False:

                        # si c'est le cas on rajoute ce couple dans la liste des couples de sommets deconnecte 
                        disconnected_pairs.append(couple)

                # en faisant cela on aura les couples de sommets en double avec juste l'ordre qui change
                # par exemple si le sommet 1 et 2 sont deconnecte on aura dans la liste:
                # [[1,2],[2,1]] or on veut juste garder un seul couple car ils representent la meme chose
                # pour cela on parcourt la liste des couples reelements deconnecte
                for couple_1 in disconnected_pairs:

                    # et on le reparcourt
                    for couple_2 in disconnected_pairs:

                        # si l'element 0 du couple_1 = l'element 1 du couple_2 et inversement alors les couples sont identiques
                        if couple_1[0]==couple_2[1] and couple_1[1]==couple_2[0]:

                            # on supprime le couple_2 de la liste des couples de sommets deconnecte
                            disconnected_pairs.remove(couple_2)

                # puis on retourne la liste des couples de sommets deconnecte
                return disconnected_pairs
            #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
            
            # on a definit notre fonction diconnected_pairs() pour connaitres les pairs de sommets deconnecte
            # maintenant on declare une liste qui contiendra la liste des couples de taches independantes
            tasks = []

            # on parcourt les couples de sommets non connecte
            for couple in diconnected_pairs():

                # on declare une sous liste qui contiendra les taches corespondants au sommet
                couple_task = []

                # on ajoute ces taches dans la sous liste
                couple_task.append(self.getTaskByName(couple[0]))
                couple_task.append(self.getTaskByName(couple[1]))

                # puis on met cette sous liste dans la liste tasks
                tasks.append(couple_task)

            # tasks corespond au couple de taches pour lesquelles on verifie les confditions de Bernstein
            # on parcourt cette liste
            for couple in tasks:

                # on parcourt chaque case memoire de lecture de la tache couple[0]
                for mem in couple[0].reads:

                    # et si la case memoir est dans le domaine d'ecriture de la tache couple[1]
                    if mem in couple[1].writes:

                        # on a une condition suffisante pour montrer que le systeme n'est pas deterministe
                        raise ValueError(f"systeme non deterministe: confusion entre {couple[0].name} qui lit dans {mem} quand {couple[1].name} ecrit dedans")
            
            # on fait le meme procede pour ecriture lecture
            for couple in tasks:
                for mem in couple[0].writes:
                    if mem in couple[1].reads:
                        raise ValueError(f"systeme non deterministe: confusion entre {couple[0].name} qui ecrit dans {mem} quand {couple[1].name} lit dedans")
            
            # meme procede pour ecriture ecriture
            for couple in tasks:
                for mem in couple[0].writes:
                    if mem in couple[1].writes:
                        raise ValueError(f"systeme non deterministe: confusion entre {couple[0].name} et {couple[1].name} les 2 tentent d'ecrire dedans")
            
            # si jusqu'ici il n'y a pas eu d'erreur on renvoie True car le systeme est determinist
            return True
        #'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        
        # permet de verifier que le graphe corespondant au syteme decrit est acyclique

        #'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        def isCyclic():
            try:

                # on utilise la fonction find_cycle de la bibliotheque networkx
                cycle = nt.find_cycle(self.G)

                # on retourne le resultat de cette fonction (si on retourne c'est que il y a un cycle)
                return cycle
            
            # puisque l'on retourne toujours le resultat de la fonction find_cycle il faut une exception
            # et l'execption c'est justement lorsque il n'y a pas de cycle 
            except NetworkXNoCycle:
                pass

            #auquel cas on retourne False
            return False
        #'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        
        # une fois toutes ces taches definis on peut commencer toutes nos verification
        # on verifie que le systeme de tache comporte au minimum 2 taches
        if len(self.tasks)<2:
            raise ValueError("le systeme de tache doit contenir au minimum 2 taches")
        
        # on declare un ensemble (cela va nous permettre de faire des verifications)
        tab=set()

        # on parcourt lensemble des taches
        for task in self.tasks:

            # si la tache est deja dans tab c'est qu'elle est declare en double
            if task.name in tab:
                raise ValueError(f"la tâche {task.name} existe déjà")
            
            # la tache n'est pas dans tab donc on l'ajoute
            # a la fin on se retouve avec toutes les taches du systeme
            tab.add(task.name)

        # on verifie que les dependances sont bien decrites 
        # c'est a dire que les taches dependent de taches declare qui existent dans le systeme
        # on parcour les taches
        for task in self.tasks:

            # on parcours les dependances de cette tache (telle que l'on le decrit dans le dictionnaire de precedences)
            for dep in self.getDependenciesSeq(task.name):

                # si cette dependance que l'on parcourt n'est pas dans tab c'est que la tache n'existe pas dans le systeme
                if dep not in tab:
                    raise ValueError(f"la tâche {task.name} dépend d'une tâche inconnue {dep}")
                
        # dans le couple cle valeur du dictionnaire de precedence
        # la cle est la tache qui va dependre de toutes les taches presentent dans la liste valeur
        # donc on parcourt toutes les cles
        for key in getKey():

            # si la cle n'est pas dans tache, c'est que la tache n'existe pas dans le systeme
            if key not in tab:
                raise ValueError(f"tâche {key} inconnue")
                
        # pour qu'un systeme puisse s'executer il ne faut pas que les taches s'attendent mutuellement
        # c'est l'equivalent d'un cycle si l'on represente le systeme sous forme d'un graphe
        # on verifie que le graphe du systeme decrit n'est pas cyclique
        if isCyclic() != False:
            raise ValueError("le systeme de tache forme un cycle:",  isCyclic())
        
        # pour qu'un systeme de tache soit deterministe (obtenir toujours le meme resultat pour une instance donne)
        # on peut verifier les conditions de Bernstein
        bernstein()

        # à l'issu de cette fonction, si il n'y a pas eu d'erreur c'est que le systeme est correctement declare
    #**************************************************************************************************************


    # à partir d'un nom de tache renvoie la tache en quastion
    #**************************************************************************************************************
    def getTaskByName(self, task_name):

        # on parcourt les taches 
        for task in self.tasks:

            # si le nom de la tache que l'on parcourt corespond au nom rentre en parametre
            if task.name==task_name:

                # on retourne la tache
                return task
            
        # si on a pas trouver on indique un message nous disant que la tache n'est pas presente
        return f"la tache {task_name} n'est pas presente dans le systeme"
    #**************************************************************************************************************

    
    # renvoie toutes les dependances d'une tache donnee tel que c'est decrit dans le dictionnaire de precedence
    # on s'en sert pour construire le graphe initial du systeme (tel qu'on le definit)
    #**************************************************************************************************************
    def getDependenciesSeq(self, nomTache):

        # si la tache est presente dans le systeme on renvoie son dictionnaire de precedence
        if self.getTaskByName(nomTache) in self.tasks:
            return self.precedence_dico.get(nomTache,[])
        
        # sinon on renvoie le message renvoye par la fonction getTaskByName
        return self.getTaskByName(nomTache)
    #**************************************************************************************************************
    
    
    # affiche le graphe de precedence du systeme (non parallelise)
    #**************************************************************************************************************
    def drawSeq(self):

        # on verifie d'abord que le systeme est correctement definit
        self.Erreur()
        
        # on utilise la fonction_circular layout pour que le graphe soit plus lisible
        nt.draw(self.G, pos=nt.circular_layout(self.G), with_labels=True)
        mp.show()
    #**************************************************************************************************************
    

    # fonction qui execute le systeme de facon sequentielle
    #**************************************************************************************************************
    def runSeq(self):

        #on verifie d'abord que le systeme est correctement definit avant de l'executer
        self.Erreur()

        # on definit ensuite 2 fonctions:
            # run_task(task)            ligne 400
            # get_task_state(task_name) ligne 422

        # c'est cette fonction qui va etre appele pour executer une tache
        #'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        def run_task(task):

            # on verifie que pour la tache que l'on veut executer, toutes les taches dont elle depend ont ete execute

            if all(get_task_state(dep) for dep in self.precedence_dico.get(task.name, [])):

                # message indiquant le debut d'execution de la tache
                print(f"doing : {task.name}")

                #on lance la fonction run propre a chaque tache
                task.run()

                # on passe sont statut a True pour dire que la tache a ete execute
                task.state = True

                # on affiche un message indiquant que la tache est fini
                print(f"{task.name} finished")
        #'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

        # fonction qui nous permet de savoir si une tache a ete execueter ou non (avec son nom donne en parametre)
        #'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        def get_task_state(task_name):

            # on parcourt toutes les taches
            for task in self.tasks:

                # si le nom de la tache correspond au nom donne en parametre
                if task.name == task_name:

                    # on retourne le statut de la tache
                    return task.state
                
            # par defaut on retourne False
            return False
        #'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

        # unfois ces 2 fonctions definis ont peut commencer l'execution
        # on marque le temps de debut
        start = time.time()

        # tant que toutes les taches du systeme n'ont pas ete execute
        while not all(get_task_state(task.name) for task in self.tasks):

            # on parcourt chaque tache du systeme
            for task in self.tasks:

                # si elle n'a pas ete execute
                if task.state==False:

                    # on lance l'execution de la tache
                    run_task(task)

        # toutes les taches ont ete execute, on marque le temps de fin 
        end = time.time()

        # pour chaque tache on remet le statut a False (cas où l'on voudrait faire une deuxieme execution à la suite)
        for task in self.tasks:
            task.state = False

        # on retourne le temps d'execution (cela va nous servir pour comparer le temps avec l'execution parallele)
        return end-start
    #**************************************************************************************************************

    
    # pour construire un systeme de tache a paralelisme maximal on construit d'abord un tableau (matrice carre)
    # nous indiquant les paires de tâches en interférence sur les accès à la mémoire
    # c'est ce que fais cette fonction
    #**************************************************************************************************************
    def interference (self):

        # on declare une liste vide qui sera à la fin le tableau des interferences entre taches
        # cette liste est de la forme d'une liste de liste ou chaque element de cette sous liste corespond
        # a un couple de deux valeurs qui seront le nom de 2 taches en interference memoire
        # pour faciliter par la suite la construction du systeme, la tache de gauche dans le couple
        # sera la tache celle qui s'executera en premier par rapport a la tache de droite
        # et pour savoir cela justement on utilisera par la suite la fonction order() declarer ci-dessous
        # cet element est utile pour connaitre les dependances entre taches dans notre systeme de paralelisme maximal

        # donc avant de commencer on va d'abord definir notre fonction order()
        # cette fonction renvoie la liste des taches du systeme suivant l'ordre de precedence
        # elle suit le meme principe que l'execution sequentielle
        # au lieu de lancer une execution de tache on va l'ordonne

        # avant de faire tout cela on verifie d'abord que notre systeme de tache est valide
        self.Erreur()

        #'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        def order():

            # pour ordoner toutes nos taches il faut definir 2 fonctions :
                # order_task(task)                  ligne 496
                # get_task_order(task_name)         ligne 504


            # fonction qui va ordonner une tache 
            # meme principe que run_task()
            #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
            def order_task(task):
                if all(get_task_order(dep) for dep in self.precedence_dico.get(task.name, [])):
                    task.ordered = True
                    self.ordered_tasks.append(task)
            #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

            # renvoie si une tache est ordonne ou non (meme principe que get_task_state())
            #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
            def get_task_order(task_name):
                for task in self.tasks:
                    if task.name == task_name:
                        return task.ordered
                return False
            #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


            while not all(get_task_order(task.name) for task in self.tasks):
                for task in self.tasks:
                    if task.ordered==False:
                        order_task(task)
            return self.ordered_tasks
        #'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

        tabInter = []

        # tout d'abord on initialise toutes les cases a 0
        # utile pour faire des calculs par la suite avec les liste car on connaitra la taille
        # on parcourt la liste des taches
        for i in range(len(self.tasks)):

            # pour chaque tache on declare une liste 
            # liste de couple où la tache de gauche sera la tache i 
            # et celle de droite avec laquelle elle est en interference memoire
            ligne = []

            # on parcourt une deuxieme fois le tableau
            for j in range(len(self.tasks)):

                # on declare une sous liste qui sera une liste de taille 2 (couple)
                sous_ligne = []

                # et donc pour k allant de 0 à 2
                for k in range(2):

                    # on inscrit 0 dans la case
                    sous_ligne.append(0)

                # on ajoute cette sous liste à la liste de la tache i
                ligne.append(sous_ligne)

            # et on ajoute la liste de la tache i au tableau final
            tabInter.append(ligne)

        # et maintenant avant de trouver les interferences on ordonne les taches de notre systeme
        order()

        # 2 taches sont en interference si :
        # l'une lit dans une case memoire tandis que l'autre ecrit dedans
        # l'une ecrit tandis que l'autre lit dedans
        # les 2 ecrivent dans une meme case memoire

        # on verifie d'abord cette condition :
        # une tache lit dans une case memoire tandis que l'autre ecrit dedans
        # de la meme maniere qu'au dessus on parcourt notre liste de taches (ordonne cette fois ci)
        for i in range(len(self.ordered_tasks)):

            # on parcourt la liste du domaine de lecture de la tache i
            for j in range(len(self.ordered_tasks[i].reads)):

                # on parcourt la liste des taches (ordonne) en commencant a i+1
                # on commence a i+1 car la tache i sera la meme que la tache k=0
                for k in range(i+1, len(self.ordered_tasks)):

                    # on parcourt le domaine d'ecriture de la tache k
                    for l in range(len(self.ordered_tasks[k].writes)):

                        # si on est surla meme case memoire 
                        # (case l du domaine d'ecriture de la tache k egal à case j du domaine de lecture de la tache i)
                        if self.ordered_tasks[k].writes[l]==self.ordered_tasks[i].reads[j]:

                            # on ecrit dans la sous liste de tabInter[i][k]
                            # tabInter[i] correspond a la liste de la tache i
                            # tabInter[i][k] corespond a l'element k de la liste tabInter[i] (couple)
                            # et donc dans ce couple l'element de gauche (tabInter[i][k][0]) sera le nom de la tache i
                            # et l'element de droite le nom de la tache k
                            tabInter[i][k][0] = self.ordered_tasks[i].name
                            tabInter[i][k][1] = self.ordered_tasks[k].name

        # on repete l'operation pour verifier cette fois-ci si cette condition :
        # une tache ecrit dans une case memoire tandis que l'autre lit dedans

        for i in range(len(self.ordered_tasks)):
            for j in range(len(self.ordered_tasks[i].writes)):
                for k in range(i+1, len(self.ordered_tasks)):
                    for l in range(len(self.ordered_tasks[k].reads)):
                        if self.ordered_tasks[k].reads[l]==self.ordered_tasks[i].writes[j]:
                            tabInter[i][k][0] = self.ordered_tasks[i].name
                            tabInter[i][k][1] = self.ordered_tasks[k].name

        # on repete une derniere fois l'operation pour verifier la condition suivante :
        # 2 taches ecrivent dans une meme case memoire                    

        for i in range(len(self.ordered_tasks)):
            for j in range(len(self.ordered_tasks[i].writes)):
                for k in range(i+1, len(self.ordered_tasks)):
                    for l in range(len(self.ordered_tasks[k].writes)):
                        if self.ordered_tasks[k].writes[l]==self.ordered_tasks[i].writes[j]:
                            tabInter[i][k][0] = self.ordered_tasks[i].name
                            tabInter[i][k][1] = self.ordered_tasks[k].name

        # une fois tout cela finis on retourne notre tableau
        return tabInter
    #**************************************************************************************************************
    

    # fonction qui va renvoyer les dependances d'une tache dont le nom est donne en parametre
    # selon le système de parallélisme maximal
    # c'est a dire la liste des taches qui doivent s'executer avant la tache dont le nom est donne en parametre
    #**************************************************************************************************************
    def getDependencies(self,nomTache):

        # on verifie d'abord que le nom de la tache donne se trouve dans le systeme
        if self.getTaskByName(nomTache) in self.tasks:
            # on declare une liste vide (ce sera la liste des dependances)
            l = []

            # on parcourt les taches
            for task in self.tasks:

                # si on est sur la tache dont le nom est donne en parametre
                if task.name==nomTache:

                    # on parcourt chaque tache
                    for i in range(len(self.tasks)):

                        # pour chaque tache on reparcourt chaque tache
                        # on le fais 2 fois car nortre tableau inter est a 2 dimension
                        for j in range(len(self.tasks)):

                            # si dans le tableau d'interference, a la case [i][j][1] il y a le nom de la tache qu'on paarcourt
                            # self.interference()[i] correspond a la liste des interferences de la tache i
                            # self.interference()[i][j] corespond au couple d'interference entre la tache i et j
                            # donc si dans ce couple (liste de 2 elements) a la case [1] il y a le nom de la tache que l'on parcourt
                            # ca veut dire que la tache i depend de la tache j qui est le nom de la tache que l'on parcourt 
                            # voir cela comme un parcourt d'un tableau a 2 dimension :
                            # la tache i est la ligne et la tache j colonne
                            # dans la case [i][j] il y aura donc le couple d'interference (si i et j sont interferente)
                            # on verifie toujours le nom avec [i][j][1], on peut se le permettre car
                            # lors de la creation du tableau d'interference on a parcouru les taches dans l'ordre d'execution
                            # cela veut dire que l'on a toujours mis a droite (case 1) la tache qui devait s'executer
                            # apres la tache de gauche (case 0)
                            if self.interference()[i][j][1]==task.name:

                                # alors on l'ajoute dans notre liste de dependance
                                l.append(self.interference()[i][j][0])

            # on renvoie la liste des dependances
            return l
        
        # la tache n'est pas dans le syteme, on renvoie le message renvoye par la fonction getTaskByName
        return self.getTaskByName(nomTache)
    #**************************************************************************************************************


    # fonction qui va executer le systeme en paralelisant les taches qui peuvent l'etre
    #**************************************************************************************************************
    def run(self):

        # on verifie que le systeme est bien defini
        self.Erreur()

        # avant d'executer le systeme il nous faut definir plusieurs fonctions:
        # const_paral()             ligne 675
        # run_task(task)            ligne 708
        # can_run(task)             ligne 719
        # getNext(task)             ligne 731

        # fonction qui va renvoyer le dictionnaire de precedence dans le cas du paralelisme maximal
        #'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        def constr_para():

            # on declare un ensemble qui va corespondre au nouveau dictionnaire de precedence
            newPrecedenceDico = {}

            # pour chaque tache du systeme
            for task in self.tasks:

                # on declare une liste qui corespondra aux dependances de la tache que l'on parcourt
                l = []

                # pour i allant de 0 a la longueur de la liste
                for i in range(len(self.tasks)):

                    # pareil pour j
                    for j in range(len(self.tasks)):

                        # si la tache que l'on parcourt est dans interference()[i][j][1]
                        # alors cette tache est en interference avec la tache interference()[i][j][0]
                        if self.interference()[i][j][1]==task.name:

                            # on ajoute donc interference()[i][j][0]
                            l.append(self.interference()[i][j][0])

                # on ajoute dans le nouveau dictionnaire la cle task.name et ses dependances l
                newPrecedenceDico[task.name] = l

            # puis on renvoie ce dictionnaire
            return newPrecedenceDico
        #'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        
        # c'est cette fonction qui va etre appele pour executer une tache
        #'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        def run_task(task):

            # elle affiche un message quand la tache va commence
            print(f"doing {task.name}")

             # puis lance son execution
            task.run()
        #'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

        # verifie si une tache peut etre execute
        #'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        def can_run(task):

            # on recupere les dependances de la tache (du systeme parallelise)
            dependencies = self.precedence_dico_paral.get(task.name, [])

            # renvoie vraie si toutes les taches dont depend la tache rentre en parametre ont ete execute
            # task_executed represente un ensemble de tache qui ont deja ete execute jusqu'a present
            return all(dependency in tasks_executed for dependency in dependencies)
        #'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

        # fonction qui renvoie pour une tache les taches qui dependent d'elle (inverse de getDependencies())
        #'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        def getNext(task):

            # on declare une liste (corespond aux taches qui dependent de la tache task)
            next = []

            # on parcourt les taches du systeme
            for t in self.tasks:

                # si la tache donne en parametre est dans les dependances de t
                if task.name in self.getDependencies(t.name):

                    # t depend de la tache donne en parametre, on rajoute donc le nom de la tache t dans next
                    next.append(t.name)

            # on retourne notre liste 
            return next
        #'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

        # une fois toutes les fonctions declare
        # on construit notre nouveau dictionnaire de precedence corespondant au systeme paralelise 
        # on met ce dictionnaire dans precedence_dico_paral du systeme de tache
        self.precedence_dico_paral=constr_para()

        # on defini un ensemble qui va corespondre aux taches execute
        tasks_executed = set()

        # puis on commence l'execution donc on va marquer le temps du debut d'execution
        start = time.time()

        # tant la longueur de task_executed est inferieur a la longueur de de la liste de taches du syteme de tache
        # cela veut dire que toutes les taches n'ont pas encore ete execute
        while len(tasks_executed) < len(self.tasks):

            # on cree une liste qui va accueillir des couples thread/tache que le thread execute
            threads = []

            # puis on parcourt les taches de notre systeme
            for task in self.tasks:

                # si la tache peut etre execute et qu'elle n'a pas encore ete execute
                if can_run(task) and task.name not in tasks_executed:

                    # on creer une petite sous liste qui va accueillir un thread et la tache qu'il execute
                    t = []

                    # on creer un thread qui va executer la fonction run_task pour la tache task
                    thread = threading.Thread(target=run_task, args=(task,))

                    # on rajoute dans t le thread puis la tache qu'il execute
                    t.append(thread)
                    t.append(task)

                    # on met dans le tableau de threads t
                    threads.append(t)

                    # puis on lance le thread
                    thread.start()
            
            # on parcourt notre tableau de threads
            for thread in threads:
                
                # on attend que le thread termine
                thread[0].join()

                # on affiche un message disant le thread est fini
                print(f"{thread[1].name} finished")

                # et on ajoute le nom de la tache dans la liste des tache execute
                tasks_executed.add(thread[1].name)

                # on regarde si il ya des taches qui dependent de la tache qui vient d'etre execute
                # on fait cela car dans l'eventualite ou une tache peut directement etre execute apres celle qui vient de finir
                # sans attendre les autres taches en cours d'execution
                if getNext(thread[1]):

                    # on parcourt les taches qui dependent de la tache fini
                    for tas in getNext(thread[1]):

                        # si une tache peut etre executer on l"execute (meme maniere que plus haut)
                        if can_run(self.getTaskByName(tas)):
                            l = []
                            t = threading.Thread(target=run_task, args=(self.getTaskByName(tas),))
                            l.append(t)
                            l.append(self.getTaskByName(tas))
                            threads.append(l)
                            t.start()

        # on marque le temps de fin puis on renvoie la duree total d'execution
        end = time.time()
        return end-start
    #**************************************************************************************************************
    

    # fonction pour afficher le graphe de precedence du systeme de paralelisme maximal
    #**************************************************************************************************************
    def draw(self):

        # de la meme maniere que l'on a cree le graphe de precedence du systeme, on cree un graphe oriente
        # la seule difference c'est que cette fois ci on prend la fonction getDependencies() qui se base 
        # sur le systeme de paralelisme maximal
        G= nt.DiGraph()
        for task in self.tasks:
            G.add_node(task.name)
            for dep in self.getDependencies(task.name):
                G.add_edge(dep,task.name)

        # la fonction nt.algorithms.dag.transitive_reduction(G) permet de supprimer les arcs redondants 
        nt.draw(nt.algorithms.dag.transitive_reduction(G), pos=nt.circular_layout(G), with_labels=True)
        mp.show()
    #**************************************************************************************************************       


    # fonction qui va executer le systeme de facon paralelle un certain nombre de fois
    # avec des valeurs aleatoire pour les variables (cases memoire)
    #**************************************************************************************************************
    def detTestRnd(self, nb_exec):

        # on declare 2 listes
        var = [] # va contenir la liste des cases memoire utiliser par le systeme
        verif = [] # va contenir les valeurs des variables apres chaque execution

        # on parcourt les taches du systeme
        for task in self.tasks:

            # on parcourt les cases memoire du domaine de lecture de la tache
            for mem in task.reads:

                # si elle n'est pas deja dans var on la met
                if mem not in var:
                    var.append(mem)
            
            # on fait pareil pour le domaine d'ecriture
            for mem in task.writes:
                if mem not in var:
                    var.append(mem)

        # on parcourt les variables
        for mem in var:

            # on leur attribut des valeurs aleatoire entre 1 et 10
            setattr(memory, mem, random.randint(0, 10))

        random_val = [] # va contenir la liste des valeurs des variables avec leur nom
        val_stock = [] # va contenir la liste des valeurs 
        # on fait cela car apres chaque execution les valeurs des variables global vont change et donc
        # si on veut reexceuter le systeme avec les meme valeurs des variables globals il faut les stocker

        # on parcour nos variables
        for v in var:
            random_val.append(f"{v} = {getattr(memory, v)}")
            val_stock.append(getattr(memory, v))

        # message pour expliciter l'execution
        print(f"execution paralleles avec les valeurs aleatoires suivantes: {random_val}")
        print("")

        # on va repeter nb_exec fois ce bloc :
        for i in range(nb_exec):

            # execution paralele du systeme
            self.run()

            # liste pour stocker les valeurs des variables apres execution
            new_val = []

            # pour chaque variable
            for val in var:

                # on recupere sa valeur que l'on met dans new_val
                new_val.append(f"{val} = {getattr(memory, val)}")

            # on verifie que la liste des valeurs n'est pas deja dans verif, et si c'est le cas on rajoute
            # la liste des valeurs sera surement dans verif apres la deuxieme execution
            # vu que le systeme est cense etre deterministe et donc renvoye le meme resultat
            if new_val not in verif:
                verif.append(new_val)

            # on affiche nos valeurs
            print(f"valeurs des variables apres execution {i+1} : {new_val}")
            print("")

            # on remets les valeurs de nos variables globals telles qu'elles avaient ete initialise aleatoirement
            i = 0
            for mem in var:
                 
                 # on se sert de val_stock
                 setattr(memory, mem, val_stock[i])
                 i = i+1

        # a la fin de l'execution si verif est plus grand que 1 c'est qu'il y a eu 2 liste de valeurs differentes
        # donc pour un meme jeu de valeurs 2 executions ont donne un resultat differents
        # on affiche un message explicite en fonction de notre cas
        if len(verif)==1:
            print("system determinist")
        else:
            print(f"system non determinist, valeurs differentes : {verif} pour meme execution {random_val}")
    #**************************************************************************************************************


    # fonction qui va execute sequentiellement et paralelement un systeme un certain nombre de fois
    # et nous dire le temps moyen d'execution pour chaque type d'execution (sequentielle et parallele)
    #**************************************************************************************************************
    def parCost(self, nb_exec):

        # on initialise le temps a 0
        seq = 0
        par = 0

        # on execute d'abord un certains nombre de fois en sequentiel
        for i in range (nb_exec) :

            # on somme la duree d'execution
            seq = seq + (self.runSeq())

        # puis on calcul la moyenne
        seq = seq/nb_exec

        # pareil pour execution paralelle
        for i in range (nb_exec) :
            par = par + (self.run())
        par = par/nb_exec

        # on affiche les differents temps
        print(f"temps d'execution moyenne en sequentielle pour {nb_exec} executions : {seq} ms")
        print(f"temps d'execution moyenne en parallele pour {nb_exec} executions : {par} ms")
    #**************************************************************************************************************
#-----------------------------------------------------------------------------------------------------------------
    




            
            

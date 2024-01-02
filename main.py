import time
import sys
from collections import Counter

#------------------------------------------  FONCTIONS  ------------------------------------------

# Traduire le graphe en dictionnaire

def mon_graphe (file) :
    info = (file[0].split() [0], file[0].split() [1])
    G = dict()
    i=1
    n=1
    while (i <= len (file)-1):
        line = file [i]
        t = line.split()
        if ('%' not in t) :
            G[str(n)] = t
            n+=1
        i+=1
    return G, info

# Permet de détecter tous les cycles d'un graphe (utilisé pour les petits graphes)
 
def ArcA(graph):
    global start
    stack = []
    discovery_time = {}
    back_edges = set()
    t = 1
    
    for node in graph :
        if node not in discovery_time and node not in back_edges :
            discovery_time[node] = t
            stack.append(node)

            while stack:
                current = stack[-1]
                t +=1
                end = time.time ()
                if (end - start > 595) : # Arrête la recherche si le programme dure plus de 595 secondes
                    return {-1}
                for neighbor in graph [current] :
                    if (neighbor not in discovery_time) :
                        stack.append(neighbor)
                        discovery_time[neighbor] = t
                        break
                    elif (neighbor in stack) :
                        back_edges.add(current)
                        break
                if (stack[-1] == current) :
                    stack.pop()
                    
                t += 1

    return back_edges

# Retourne le 'second' noeud de chaque arc arrière d'un DFS (utilisé pour les petits graphes)

def ArcA_Bis(graph, start):
    stack = []
    discovery_time = {}
    back_edges = []
    t = 0

    stack.append(start)

    while stack:
        current = stack.pop()
        if current not in discovery_time:
            t += 1
            discovery_time[current] = t
            stack.append(current)
            
            for neighbor in graph[current]:
                if neighbor not in discovery_time:
                    stack.append(neighbor)
                elif (neighbor in stack) :
                    back_edges.append(neighbor)

            t += 1

    return back_edges

# Fonctions permettant de vérifier si il y a toujours un arc arrière dans un DFS (utilisé pour les petits graphes)

def ArcA_Bis2 (graph, start):
    stack = []
    discovery_time = {}
    t = 0

    stack.append(start)

    while stack:
        current = stack.pop()
        if current not in discovery_time:
            t += 1
            discovery_time[current] = t
            stack.append(current)
            
            for neighbor in graph[current]:
                if neighbor not in discovery_time:
                    stack.append(neighbor)
                elif (neighbor in stack) :
                    return True

            t += 1

    return False

# Detection de cycles (utilisé pour les petits graphes) : vérifie si il y a encore des arcs arrières !

def IsThereACycle (G) :
    for node in G : 
        if ArcA_Bis2 (G,node) :
            return True
    return False
    
# Noeuds sur lesquels il y a un cycle (pour les petits graphes)

def CoupeMin (G) :
    allArcs = []
    for noeud in G :
        allArcs+=ArcA_Bis (G,noeud) # Recense tous les arcs arrières de tous les DFS
    allCNtemp = Counter(allArcs).most_common() # Renvoie une liste de tuples de type (noeud,nombre d'apparition dans allArcs), la liste de tuple est triée selon le nombre d'apparition
    allCN = [x[0] for x in allCNtemp] # Renvoie une liste avec les sommets seulement
    return allCN

# Supprimer un noeud d'un graphe

def Supprimer_Noeud (G,a) : 
    for node in G :
        while a in G[node] :
            G[node].remove(a)
    G.pop(a)

# (En retournant la valeur du noeud supprimée : utile pour supprimer les noeuds tout en les ajoutant à l'ensemble de sommets à supprimer dans le sous-programme 2)
    
def Supprimer_Noeud_Bis (G,a) : 
    for node in G :
        while a in G[node] :
            G[node].remove(a)
    G.pop(a)
    return a

# Détecter les noeuds dont le degré sortant est 0

def Nettoyer_Graphe (G) : 
    l = []
    for node in G :
        if (G[node] == []) :
            l.append(node)
    return l
            
#------------------------------------------  PROGRAMME PRINCIPAL  ------------------------------------------
file = sys.stdin.readlines()
start = time.time()

#print ("Lecture du graphe")
lecture = mon_graphe(file)
graph = lecture [0]
info = lecture [1]

EnsembleMin = set()

#------------------------------------------ SOUS-PROGRAMME 1 : GRANDS GRAPHES ------------------------------------------ 
if (int(info[0]) >= 3000) : # A partir de 3000 sommets, on considère le graphe comme 'grand'
    
    #print("Recherche de l'ensemble de sommets à supprimer")
           
    EnsembleMin = ArcA(graph)

#------------------------------------------ SOUS-PROGRAMME 2 : PETITS GRAPHES ------------------------------------------
else : # En dessous de 3000 noeuds, le graphe est 'petit'
    
    #print ("Recherche des noeuds dont le degré sortant est 0 : on allège le graphe")
    
    noeuds_inutiles = Nettoyer_Graphe(graph)
    for i in noeuds_inutiles :
        Supprimer_Noeud(graph,i)  
    
    #print("Recherche de l'ensemble minimal de sommets à supprimer")
    
    CMIN = CoupeMin(graph)
    i=0

    while IsThereACycle(graph) :
        end = time.time()
        if (end - start > 595) : # Arrête la recherche si le programme dure plus de 595 secondes
            EnsembleMin = {-1}
            break
        EnsembleMin.add(Supprimer_Noeud_Bis(graph, CMIN[i]))
        i+=1

#------------------------------------------ Ecriture du résultat dans le fichier 'Solution' ------------------------------------------
if EnsembleMin == {-1} : # On print tout le graphe si 10 minutes n'ont pas suffit à rendre le graphe acyclique
    for x in range (1,int(info[0]) + 1) :
        print (str(x))
else :
    for k in EnsembleMin : 
        print (k)
        
#print (str(len(EnsembleMin)) + " sommets ont été supprimés afin de rendre le graphe acyclique")

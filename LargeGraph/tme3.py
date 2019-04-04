import matplotlib.pyplot as plt
import numpy as np
import time

def cptNodeEdge(fileName):
    f = open(fileName,'r')
    nbE = 0;
    nodeSeen = set()
    for line in f:
        s = line.split()
        nbE = nbE + len(s) -1
        for a in s:
            nodeSeen.add(a)
    del s
    nbN = len(nodeSeen)
    del nodeSeen
    return nbN,nbE


#tail -n +5 nileName >> ~/S2/CPA/tme3/fileNameN 
#sort -g fileNameN|uniq > PasDouble
#sort -g amazon_ungraphClean.txt > amazon_ungraphClean2.txt 

def dictClean(f):
    res = {}
    for line in f:
        if(line[0] == '#'):
            continue
        
        s = line.split()
        for i in range(len(s)-1):
            if(s[i] != s[i+1]):
                  if(s[i] in res):
                    res[s[i]].append(s[i+1]) 
                  else:
                     res[s[i]] = list(s[i+1])
         
    w = list()
    for cle in res.keys():
        val = res[cle]
        for k in val:
            if(k in res):
                if(cle in res[k]):
                    res[k].remove(cle)
            else:
                w.append(k)
    for i in w:
        res[i] = list()
    return res

def clean(fileName):
    
    f = open(fileName,'r')
    res = dictClean(f)
    f.close()
    
    f = open(fileName[:-4]+"Clean.txt","a")
    for cle in res.keys():
        if(len(res[cle]) == 0):
            continue
        else:
            for k in res[cle]:
                f.write(cle+" "+k+"\n")
    f.close()


def degree(fileName):
    f = open(fileName,'r')
    deg ={}
    for line in f:
        s = line.split()
        for i in range(len(s)-1):
            if(s[i] in deg):
                deg[s[i]] += 1
            else:
                deg[s[i]] = 1
            if(s[i+1] in deg):
                deg[s[i+1]] += 1
            else:
                deg[s[i+1]] = 1

    return deg

def quantity(fileName):
    deg = degree(fileName)
    f = open(fileName,'r')
    q = 0
    for line in f:
        s = line.split()
        for i in range(len(s)-1):
            q += deg[s[i]]*deg[s[i+1]]
    return q

def degDist(fileName):
    d =degree(fileName)
    dist = {}
    for k in d.keys():
        if(d[k] in dist):
            dist[d[k]] += 1
        else:
            dist[d[k]] = 1
            
    f = open(fileName[23:-4]+"DegDist.txt","a")
    for cle in dist.keys():
        f.write(str(cle)+" "+str(dist[cle])+"\n")
    f.close()
    f = open(fileName[23:-4]+"DegDist.txt","r")
    x = list()
    y = list()
    for line in f:
        s = line.split()
        x.append(int(s[0]))
        y.append(int(s[1]))
    f.close()
    plt.scatter(x,y)
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("degree")
    plt.ylabel("nb Nodes")
    plt.savefig(fileName[23:-4]+"DegDist.png")
    plt.title(fileName[23:-4]+" Distribution des degrees")
    plt.show()

def adjArray(fileName):
    f = open(fileName,"r")
    res = {}
    for line in f:
        if(line[0] == '#'):
            continue
        
        s = line.split()
        for i in range(len(s)-1):
            if(s[i] != s[i+1]):
                if(s[i] in res):
                    res[s[i]].add(s[i+1])
                else:
                    res[s[i]] = set()
                    res[s[i]].add(s[i+1])
                    
                if(s[i+1] in res):
                    
                    res[s[i+1]].add(s[i])
                else:
                    res[s[i+1]] = set()
                    res[s[i+1]].add(s[i])
                    
    return res

def adjMatrix(fileName):
    f = open(fileName,"r")
    maximum = 0
    for line in f:
        s=line.split()
        m = max(int(s[0]),int(s[1]))
        maximum = max(maximum,m)
    mat = np.zeros((maximum, maximum ))
    f.close()
    f = open(fileName,"r")
    for a in f:
        s=a.split()
        i = int(s[0])-1
        j = int(s[1])-1
        mat[i][j] = 1
        mat[j][i] = 1
        mat[i][i] = 0
        mat[j][j] = 0
        
    return mat

def edgeArray(fileName):
    f = open(fileName, "r")
    edges = list()
    for line in f:
        edge=line.split()
        if(len(edge)>1):
             edges.append(edge)
    f.close()
    return edges
    
def BFS(graph, start):
   explored = []
   queue = [(start)]
   while queue:
       node = queue.pop(0)
       if node not in explored:
           explored.append(node)
           
           if str(node) in graph:
               neighbours = graph[str(node)] 
           for neighbour in neighbours:               
               queue.append((neighbour))
           
   return explored

def BFS2(graph, start):
   explored = []
   queue = [(start,0)]
   d = dict()
   d[start] = 0
   maxi = (start,0)
   while queue:
       node = queue.pop(0)
       if node[0] not in explored:
           explored.append(node[0])
           
           if str(node[0]) in graph:
               neighbours = graph[str(node[0])]
           for neighbour in neighbours:
               if(neighbour not in d):
                   if(neighbour not in d):
                       d[neighbour] = node[1]+1
                       if(maxi[1]<d[neighbour]):
                           maxi = (neighbour,d[neighbour])
               queue.append((neighbour,node[1]+1))
   return explored,maxi

def exo8(fileName):
    G = adjArray(fileName)
    
    res = list()
    key = list()
    
    for c in G.keys():
        if(c not in key):
            a = BFS(G,c)
            res.append((a,len(a)))
            for i in a:
                key.append(i)

    return res

def largestConnectedComp(fileName):
    G = adjArray(fileName)
    
    res = list()
    key = list()
    
    for c in G.keys():
        if(c not in key):
            a = BFS(G,c)
            res.append((a,len(a)))
            for i in a:
                key.append(i)
    maximum = 0
    
    for i in range (len(res)):
        if(res[i][1]>maximum):
            maximum = res[i][1]
            res2 = res[i]
    return res2

def lowerBound(fileName,nbIter):
    g = largestConnectedComp(fileName)
    p = g[0][0]
    G = adjArray(fileName)
    maxi = 0
    for i in range(nbIter):
        bfs2,c = BFS2(G,p)
        if(c[1]>maxi):
            maxi = c[1]
            p = c[0]
    return maxi

def allTriangles(filesName):
    res = list()
    edges = edgeArray(filesName)
    adj = adjArray(filesName)
    b = '0'
    for edge in edges:
        u = adj[edge[0]]
        v = adj[edge[1]]
        
        w = u.intersection(v)
        
        if((b == edge[0] or (b==edge[1]))):
                continue
        for a in w:
            l = list()
            l.append(edge[0])
            l.append(edge[1])
            l.append(a)
            l.sort()
            if(l in res):
                continue
            res.append(l)       
            quantity
    return res

#Quantity : 
# /Vrac/TME_CPA_19-02-20/email-Eu-core-clean.txt : 88109182 0.024881839752197266
# /Vrac/TME_CPA_19-02-20/com-amazon.ungraph-clean.txt : 103415531 1.5718021392822266
# /Vrac/TME_CPA_19-02-20/com-lj.ungraph-clean.txt : 789000450609 58.566508054733276
# /Vrac/TME_CPA_19-02-20/com-orkut.ungraph-clean.txt : 22292678512329 200.53568148612976
# /Vrac/TME_CPA_19-02-20/com-friendster.ungraph.txt: 379856554324947, 4390.462798095187

#d =time.time()
#q = quantity("/Vrac/TME_CPA_19-02-20/com-friendster.ungraph.txt")
#f = time.time()
#temps = f - d
#print(str(q)+" "+str(temps))
#Plot :
#degDist("/Vrac/TME_CPA_19-02-20/email-Eu-core-clean.txt")
#degDist("/Vrac/TME_CPA_19-02-20/com-amazon.ungraph-clean.txt")
#degDist("/Vrac/TME_CPA_19-02-20/com-lj.ungraph-clean.txt")
#degDist("/Vrac/TME_CPA_19-02-20/com-orkut.ungraph-clean.txt")
#degDist("/Vrac/TME_CPA_19-02-20/com-friendster.ungraph.txt") 

#Load a graph in memomry:
#edges list :
# /Vrac/TME_CPA_19-02-20/email-Eu-core-clean.txt : 0.01457236289978027
# /Vrac/TME_CPA_19-02-20/com-amazon.ungraph-clean.txt : 1.353329181671143
# /Vrac/TME_CPA_19-02-20/com-lj.ungraph-clean.txt : 1248.564356843643468
# /Vrac/TME_CPA_19-02-20/com-orkut.ungraph-clean.txt : ram pleine pc bloqué
# /Vrac/TME_CPA_19-02-20/com-friendster.ungraph.txt: 
#d =time.time()
#t = edgeArray("/Vrac/TME_CPA_19-02-20/com-lj.ungraph-clean.txt")
#f = time.time()
#print(f-d)

#adjMatrix :
# /Vrac/TME_CPA_19-02-20/email-Eu-core-clean.txt : 0.09201383590698242
# /Vrac/TME_CPA_19-02-20/com-amazon.ungraph-clean.txt : MemoryError
# /Vrac/TME_CPA_19-02-20/com-lj.ungraph-clean.txt : 
# /Vrac/TME_CPA_19-02-20/com-orkut.ungraph-clean.txt :
# /Vrac/TME_CPA_19-02-20/com-friendster.ungraph.txt: 
#d =time.time()
#t = adjMatrix("/Vrac/TME_CPA_19-02-20/com-amazon.ungraph-clean.txt")
#f = time.time()
#print(f - d)

#adjArray : 
# /Vrac/TME_CPA_19-02-20/email-Eu-core-clean.txt : 0.04520750045776367
# /Vrac/TME_CPA_19-02-20/com-amazon.ungraph-clean.txt : 1.8801968097686768
# /Vrac/TME_CPA_19-02-20/com-lj.ungraph-clean.txt : ram pleine pc bloquer
# /Vrac/TME_CPA_19-02-20/com-orkut.ungraph-clean.txt :
# /Vrac/TME_CPA_19-02-20/com-friendster.ungraph.txt: 
#d =time.time()
#t = adjArray("/Vrac/TME_CPA_19-02-20/com-lj.ungraph-clean.txt")
#f = time.time()
#print(f - d)

#largest connected component
# /Vrac/TME_CPA_19-02-20/email-Eu-core-clean.txt :  986
# /Vrac/TME_CPA_19-02-20/com-amazon.ungraph-clean.txt : 334863
# /Vrac/TME_CPA_19-02-20/com-lj.ungraph-clean.txt : ram pleine pc bloquer
# /Vrac/TME_CPA_19-02-20/com-orkut.ungraph-clean.txt :
# /Vrac/TME_CPA_19-02-20/com-friendster.ungraph.txt: 
#a = largestConnectedComp("/Vrac/TME_CPA_19-02-20/com-amazon.ungraph-clean.txt")
#print(a)
#lowerBound : 
# /Vrac/TME_CPA_19-02-20/email-Eu-core-clean.txt : 7 
# /Vrac/TME_CPA_19-02-20/com-amazon.ungraph-clean.txt : 44
# /Vrac/TME_CPA_19-02-20/com-lj.ungraph-clean.txt : ram pleine pc bloquer
# /Vrac/TME_CPA_19-02-20/com-orkut.ungraph-clean.txt :
# /Vrac/TME_CPA_19-02-20/com-friendster.ungraph.txt: 
#lower = lowerBound("/Vrac/TME_CPA_19-02-20/com-amazon.ungraph-clean.txt",4)
#print(lower)

#listing triangles 
# /Vrac/TME_CPA_19-02-20/email-Eu-core-clean.txt : 
# /Vrac/TME_CPA_19-02-20/com-amazon.ungraph-clean.txt : 
# /Vrac/TME_CPA_19-02-20/com-lj.ungraph-clean.txt : 
# /Vrac/TME_CPA_19-02-20/com-orkut.ungraph-clean.txt :
# /Vrac/TME_CPA_19-02-20/com-friadjArrayendster.ungraph.txt: 
#triangles = allTriangles("/Vrac/TME_CPA_19-02-20/email-Eu-core-clean.txt")
#print(len(triangles))

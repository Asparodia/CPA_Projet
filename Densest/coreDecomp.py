import matplotlib.pyplot as plt
import numpy as np

import minheap
  
class Graph:
    def __init__(self,fileName,Notdirected = True):
        self.fileName= fileName
        self.adj = dict()
        self.minHeap = minheap.MinHeap()
        
        self.tab = None
        
        self.nbEdge = 0
        self.nbNode = 0
        
        self.adjDirected = dict()
        
        print(" init started ")
        
        f = open(self.fileName)
        self.maxi = 0
        if(Notdirected):
            print("not a directed graph")
            for line in f:
                self.nbEdge += 1
                a = line[:-1].split()
                if(int(a[0]) == int(a[1])):
                    continue
                if(int(a[0])>self.maxi):
                    self.maxi = int(a[0])
                if(int(a[1])>self.maxi):
                    self.maxi = int(a[1])
                    
                if(int(a[0]) in self.adj):
                    self.adj[int(a[0])].add(int(a[1]))
                else:
                    self.adj[int(a[0])] = set()
                    self.adj[int(a[0])].add(int(a[1]))
                if(int(a[1]) not in self.adj):
                    self.adj[int(a[1])] = set()
                    self.adj[int(a[1])].add(int(a[0]))
                else:
                    self.adj[int(a[1])].add(int(a[0]))
                del a
            f.close()
            
            self.nbNode = len(self.adj)
            i = 1
            
            for k in self.adj.keys():
                self.minHeap.insert((k,len(self.adj[k])))
                i += 1
                
            self.tab = -1 * np.ones(self.maxi+1)
            j = 1 
            for e in self.minHeap.heapList:
                if(e[1]==-1):
                    continue
                self.tab[e[0]] = j
                j += 1
            f.close()
            print(" init done ")
        else:
            print("directed graph just for density score")
            f = open(self.fileName)
            for line in f:
                self.nbEdge += 1
                a = line[:-1].split()
                if(int(a[0]) == int(a[1])):
                    continue
                if(int(a[0])>self.maxi):
                    self.maxi = int(a[0])
                if(int(a[1])>self.maxi):
                    self.maxi = int(a[1])
                    
                if(int(a[0]) in self.adjDirected):
                    self.adjDirected[int(a[0])].add(int(a[1]))
                else:
                    self.adjDirected[int(a[0])] = set()
                    self.adjDirected[int(a[0])].add(int(a[1]))
                if(int(a[1]) not in self.adjDirected):
                    self.adjDirected[int(a[1])] = set()
            self.nbNode = len(self.adjDirected)
            
        
    def plotDegIn(self):
        print("ploting...")
        core = self.CoreDecomposition()
        x = list()
        y = list()
        for k in self.adj.keys():
            x.append(len(self.adj[k]))
            y.append(core[k][0])        
        del core
        plt.scatter(x,y,color = "red")
        plt.ylabel('coreness')
        plt.xlabel('degree')
        plt.yscale("log")
        plt.xscale("log")
        plt.title(self.fileName[:-4 ]+" coreness by degree")
        plt.savefig(self.fileName[:-4 ]+'CoreDeg.png')
        plt.show()
        del x
        del y
    
    def CoreDecomposition(self):
        print("Computing coreDecomposition for",self.fileName)
        res = dict()
        c = 0
        ind = self.minHeap.currentSize
        while self.minHeap.currentSize > 0:
            v = self.minHeap.heapList[1]
            c = max(c,v[1])
            neigs = self.adj[v[0]]
            for n in neigs:
                i = int(self.tab[n])
                if(i==-1):
                    continue
                while(i>self.minHeap.currentSize):
                    i -= 1
                
                oldDeg = self.minHeap.heapList[i][1]
                node = self.minHeap.heapList[i][0]
                
                newDeg = oldDeg - 1
                self.minHeap.heapList[i] = (node,newDeg)
                
                self.minHeap.heapList[1] = (self.minHeap.heapList[1][0],0)
                
                self.minHeap.percUp2(i,self.tab)
            
            del neigs   
            
            self.minHeap.delMin2(self.tab)
            
            res[v[0]] = (c,ind)
            ind-=1
        
        print("Computing done")
        
        a = sorted(res.items(), key = lambda x:x[1][1])
        
        tableau = np.zeros(self.maxi+1)
        delLogique = np.zeros(self.maxi+1)
        
        ind = 0
        for i in a:
            node = i[0]
            delLogique[node] = 1
            val = 0
            for j in self.adj[node]:
                if(delLogique[j] == 1):
                    val += 1 
            tableau[ind] = val
            ind += 1
        
        del delLogique
        del a
        
        maxi = 0   
        edgeDens = 0
        av = 0
        
        
        for i in range(1,tableau.size):
            tableau[i] += tableau[i-1]
            if(maxi<tableau[i]/i):
                maxi = tableau[i]/i
                if(i-1!=0):
                    edgeDens = tableau[i]/(i*(i-1))
                av = i
        
        del tableau
        
        print(self.fileName)
        print("NbNode :",self.nbNode)
        print("NbEdge :",self.nbEdge)
        print("Maximum kcore :",c)
        print("Average degre density :",maxi)
        print("Edge density :",edgeDens)
        print("densest core ordering prefix:",av)
        print("----------------------------------")        
        
        return res
    
    def flush(self):
        del self.fileName
        del self.adj 
        del self.minHeap 

def plotDegNet():
    print("ploting Net...")
    g = Graph("net.txt")
    core = g.CoreDecomposition()
    maxicore = 0            
    x = list()
    y = list()
    for k in g.adj.keys():
        x.append(len(g.adj[k]))
        y.append(core[k][0])
        if(core[k][0]>maxicore):
            maxicore = core[k][0]
    crack = list()
    for k in core:
        if(core[k][0]==maxicore):
            crack.append(k)
    del core
    plt.scatter(x,y,color = "red")
    plt.ylabel('coreness')
    plt.xlabel('degree')
    
    plt.title(g.fileName[:-4 ]+" coreness by degree")
    plt.savefig(g.fileName[:-4 ]+'CoreDeg.png')
    plt.show()
    print("la clique avec le plus grand kcore ( ",maxicore," ) : ")
    f = open("ID.txt")
    for line in f:
        s = line.split()
        if int(s[0]) in crack:
            print(s[1])
    f.close()
    del x
    del y

def densityScore(name,t):
    G = Graph(name,False)
    print("start Density score")
    r = dict()
    for i in G.adjDirected.keys():
        r[i]=0.0
    for x in range(t):
#        print("iter num :",x+1)
        for i in G.adjDirected.keys():
            for j in G.adjDirected[i]:
                if(r[i] <= r[j]):
                    r[i] += 1.0
                else:
                    r[j] += 1.0
    
    for y in r.keys():
        r[y] = r[y]/t
    
    a = sorted(r.items(), key = lambda x:x[1],reverse=True)
    print(r)
    del r
    tableau = np.zeros(G.maxi+1)
    delLogique = np.zeros(G.maxi+1)
    ind = 0
    for i in a:
        node = i[0]
        delLogique[node] = 1
        val = 0
        for j in G.adjDirected[node]:
            if(delLogique[j] == 1):
                val += 1 
        tableau[ind] = val
        ind += 1
    
    del delLogique
    del a
    
    maxi = 0   
    edgeDens = 0
    av = 0
    
    for i in range(1,tableau.size):
        tableau[i] += tableau[i-1]
        if(maxi<tableau[i]/i):
            maxi = tableau[i]/i
            if(i-1!=0):
                edgeDens = tableau[i]/(i*(i-1))
            av = i
    del tableau
    
    print(G.fileName)
    print("NbNode :",G.nbNode)
    print("NbEdge :",G.nbEdge)
    print("Average degre density :",maxi)
    print("Edge density :",edgeDens)
    print("densest core ordering prefix:",av)
    print("----------------------------------")
    
    G.flush()

def densityScoreExo4(name,t):
    f = open(name)
    maxi = 0
    for line in f:
        a = line[:-1].split()
        
        if(int(a[0])>maxi):
            maxi = int(a[0])
        if(int(a[1])>maxi):
            maxi = int(a[1])
            
    f.close()
    tab = np.zeros([(maxi+1),2],dtype='float')
    
    for x in range(t):
        f = open(name)
        for line in f:
            a = line[:-1].split()
            i = int(a[0])
            j = int(a[1])
            if(tab[i][1]<=tab[j][1]):
                tab[i][1] = tab[i][1]+1
                tab[i][0] = int(i)
            else:
                tab[j][1] = tab[j][1]+1
                tab[j][0] = int(j)
        f.close()  
    for y in range(0,maxi+1):
        tab[y][1] = tab[y][1]/t
    a = tab[tab[:,1].argsort()]
    
    del tab 
    
    delLogique = np.zeros(maxi+1)
    tableau = np.zeros(maxi+1)
    
    ind = 0
    for i in range(maxi,0,-1):
        node = a[i][0]
        delLogique[int(node)] = 1
        val = 0
        for j in range(i,0,-1):
            if(delLogique[j] == 1):
                val += 1 
        tableau[ind] = val
        ind += 1
    del delLogique
    
    maxi = 0   
    edgeDens = 0
    av = 0
    for i in range(1,tableau.size):
        tableau[i] += tableau[i-1]
        if(maxi<tableau[i]/i):
            maxi = tableau[i]/i
            if(i-1!=0):
                edgeDens = tableau[i]/(i*(i-1))
            av = i
    del tableau
    
    print(name)
    print("Average degre density :",maxi)
    print("Edge density :",edgeDens)
    print("densest core ordering prefix:",av)
    print("----------------------------------")
        

# /Vrac/TME_CPA_19-02-20/email-Eu-core-clean.txt
# /Vrac/TME_CPA_19-02-20/com-amazon.ungraph-clean.txt
# /Vrac/TME_CPA_19-02-20/com-lj.ungraph-clean.txt
# /Vrac/TME_CPA_19-02-20/com-orkut.ungraph-clean.txt
# /Vrac/TME_CPA_19-02-20/com-friendster.ungraph.txt
    
######################### EXO 1 #######################################
#g = Graph("/Vrac/TME_CPA_19-02-20/email-Eu-core-clean.txt")
#/Vrac/TME_CPA_19-02-20/email-Eu-core-clean.txt
#NbNode : 986
#NbEdge : 16064
#Maximum kcore : 34
#Average degre density : 27.691244239631338
#Edge density : 0.12820020481310804
#densest core ordering prefix: 217

#g = Graph("/Vrac/TME_CPA_19-02-20/com-amazon.ungraph-clean.txt")
#/Vrac/TME_CPA_19-02-20/com-amazon.ungraph-clean.txt
#NbNode : 334863
#NbEdge : 925872
#Maximum kcore : 6
#Average degre density : 3.9444444444444446
#Edge density : 0.23202614379084968
#densest core ordering prefix: 18

#g = Graph("/Vrac/TME_CPA_19-02-20/com-lj.ungraph-clean.txt")
#/Vrac/TME_CPA_19-02-20/com-lj.ungraph-clean.txt
#NbNode : 3997962
#NbEdge : 34681189
#Maximum kcore : 360
#Average degre density : 191.4805194805195
#Edge density : 0.49864718614718617
#densest core ordering prefix: 385

#g = Graph("/Vrac/TME_CPA_19-02-20/com-orkut.ungraph-clean.txt")
#g.CoreDecomposition()

######################################################################

###################### EXO 2 ########################################
#plotDegNet()
#NbNode : 287426
#NbEdge : 871001
#Maximum kcore : 14
#Average degre density : 10.074074074074074
#Edge density : 0.38746438746438744
#densest core ordering prefix: 27

#la clique avec le plus grand kcore (  14  ) : Un groupe d'auteur corren qui se site entre eux

#Sa-kwang
#Sung-Pil
#Chang-Hoo
#Yun-soo
#Hong-Woo
#Jinhyung
#Hanmin
#Do-Heon
#Myunggwon
#Won-Kyung
#Hwamook
#Minho
#Won-Goo
#Jung
#Dongmin
#Mi-Nyeong
#Sung
#Minhee
#Sungho
#Seungwoo
#Heekwan
#Jinhee
#Taehong
#Mikyoung
#Ha-neul
#Seungkyun
#Yun-ji

#####################################################################

##################### EXO 3 ########################################

#a = densityScore("/Vrac/TME_CPA_19-02-20/email-Eu-core-clean.txt",1000)
#/Vrac/TME_CPA_19-02-20/email-Eu-core-clean.txt
#t = 10 
#NbNode : 986
#NbEdge : 16064
#Average degre density : 21.22051282051282
#Edge density : 0.10938408670367433
#densest core ordering prefix: 195
#t = 100
#/Vrac/TME_CPA_19-02-20/email-Eu-core-clean.txt
#NbNode : 986
#NbEdge : 16064
#Average degre density : 22.569060773480665
#Edge density : 0.12538367096378147
#densest core ordering prefix: 181
#t = 1000
#/Vrac/TME_CPA_19-02-20/email-Eu-core-clean.txt
#NbNode : 986
#NbEdge : 16064
#Average degre density : 22.648936170212767
#Edge density : 0.12111730572306292
#densest core ordering prefix: 188

#a = densityScore("/Vrac/TME_CPA_19-02-20/com-amazon.ungraph-clean.txt",1000)
#t=10
#/Vrac/TME_CPA_19-02-20/com-amazon.ungraph-clean.txt
#NbNode : 334863
#NbEdge : 925872
#Average degre density : 2.4818615257048093
#Edge density : 0.00025726770246758675
#densest core ordering prefix: 9648
#t = 100
#/Vrac/TME_CPA_19-02-20/com-amazon.ungraph-clean.txt
#NbNode : 334863
#NbEdge : 925872
#Average degre density : 3.768421052631579
#Edge density : 0.04008958566629339
#densest core ordering prefix: 95
#t = 1000
#/Vrac/TME_CPA_19-02-20/com-amazon.ungraph-clean.txt
#NbNode : 334863
#NbEdge : 925872
#Average degre density : 3.5625
#Edge density : 0.0375
#densest core ordering prefix: 96
    
    
#a = densityScore("/Vrac/TME_CPA_19-02-20/com-lj.ungraph-clean.txt",1000)
#t=10
#/Vrac/TME_CPA_19-02-20/com-lj.ungraph-clean.txt
#NbNode : 3997962
#NbEdge : 34681189
#Average degre density : 168.89300582847628
#Edge density : 0.07034277627175188
#densest core ordering prefix: 2402
#t=100
#/Vrac/TME_CPA_19-02-20/com-lj.ungraph-clean.txt
#NbNode : 3997962
#NbEdge : 34681189
#Average degre density : 184.519364448858
#Edge density : 0.18341885134081312
#densest core ordering prefix: 1007

#a = densityScore("/Vrac/TME_CPA_19-02-20/com-orkut.ungraph-clean.txt",100)
#/Vrac/TME_CPA_19-02-20/com-orkut.ungraph-clean.txt
#t = 10
#NbNode : 3072441
#NbEdge : 117185083
#Average degre density : 178.81546683432882
#Edge density : 0.006246173914850106
#densest core ordering prefix: 28629
#t=100
#/Vrac/TME_CPA_19-02-20/com-orkut.ungraph-clean.txt
#NbNode : 3072441
#NbEdge : 117185083
#Average degre density : 189.1659305993691
#Edge density : 0.007459518537772353
#densest core ordering prefix: 25360
    

#/Vrac/CPA-Pagerank/alr21--dirLinks--enwiki-20071018.txt
#alr21--dirLinks--enwiki-20071018.txt
#alr21--pageNum2Name--enwiki-20071018.txt
import numpy as np
import copy as cp
import matplotlib.pyplot as plt

class PageRank:
    
    def __init__(self,fileName,alpha = 0.15):
        self.fileName= fileName
        self.alpha = alpha
        self.T = dict()
        self.Tinv = dict()
        self.P = None
        
        self.I = dict()
        
        
        print(" init started ")
        
        f = open(self.fileName)
        for line in f:
            a = line[:-1].split()
            if(int(a[0]) in self.T):
                self.T[int(a[0])].add(int(a[1]))
            else:
                self.T[int(a[0])] = set()
                self.T[int(a[0])].add(int(a[1]))
            if(int(a[1]) not in self.T):
                self.T[int(a[1])] = set()
                
            if(int(a[1]) in self.Tinv):
                self.Tinv[int(a[1])].add(int(a[0]))
            else:
                self.Tinv[int(a[1])] = set()
                self.Tinv[int(a[1])].add(int(a[0]))
            if(int(a[0]) not in self.Tinv):
                self.Tinv[int(a[0])] = set()
            del a
        f.close() 

        tmpSum = len(self.T)
        
        for i in self.T.keys():
            self.I[i] = 1/tmpSum
        
        del tmpSum
        print ("--init done ")
        
    def computation(self,nbIter):
        print( " computation start ")
        self.P = cp.deepcopy(self.I)
        
        for i in range(nbIter):
            print("------------iter nb : "+str((i+1))+" ----------")
            self.P = self.adjVectProd(self.T,self.P)
            for k in self.P.keys():
                self.P[k] =( (1-self.alpha) * self.P[k] ) + (self.alpha * self.I[k])
            self.normalize()
            print("-------------------------------------------")
        del self.I
        
        return self.P
            
    def normalize(self):
        print( " norm start ")

        t = 0
        for k in self.P.keys():
            t +=self.P[k]
        for k in self.P.keys():
            self.P[k] += ((1.0-t)/len(self.P))
        print("--norm done")
     
        
        
    def adjVectProd(self,T,P):
        print( " adjVect start ")
        res = dict()
        
        for u in T.keys():
            for v in self.Tinv[u]:
                if(v not in P):
                    continue
                degv = (len(self.T[v]))
                if((u in res)):
                    res[u] += (1/degv)*P[v]
                else:
                    res[u] = (1/(degv))*P[v]
        if(degv):
            del degv
        print("--adjVect done")
        return res
    
    def plotDegOut(self):
        
        if(not self.P):
            print("compute before plot")
            return
        x = list()
        y = list()
        for k in self.P.keys():
            x.append(self.P[k])
            y.append(len(self.T[k]))
        
        plt.scatter(x,y,color = "red")
        plt.ylabel('Out degre')
        plt.xlabel('PageRank score')
        plt.yscale("log")
        plt.xlim(0, 0.004)
        plt.title(" PageRank score per out degre ")
        plt.savefig('ScoreOut.png')
        plt.show()
        del x
        del y
        
    
    def plotDegIn(self):
        
        if(not self.P):
            print("compute before plot")
            return
        x = list()
        y = list()
        for k in self.P.keys():
            x.append(self.P[k])
            y.append(len(self.Tinv[k]))
        
        plt.scatter(x,y,color = "red")
        plt.ylabel('In degre')
        plt.xlabel('PageRank score')

        plt.yscale("log")
        plt.xlim(0, 0.004)
        plt.title(" PageRank score per in degre ")
        plt.savefig('ScoreIn.png')
        plt.show()
        del x
        del y
    

    def clean(self):
        del self.fileName
        del self.alpha
        del self.T
        del self.Tinv 
        del self.P


    
def plotAlpha(a1,a2,fileName,nbIter):
    p1 = PageRank(fileName,a1)
    p1.computation(nbIter)
    x = list()
    for k in p1.P.keys():
        x.append(p1.P[k])
        
    p1.clean()  
    
    p2 = PageRank(fileName,a2)
    p2.computation(nbIter)
    y = list()
    for k in p2.P.keys():
        y.append(p2.P[k])
    p2.clean()  
    
    plt.scatter(x,y,color = "red")
    plt.ylabel('score alpha : '+str(a2))
    plt.xlabel('score alpha : '+str(a1))
    
    plt.xlim(0, 0.010)
    plt.ylim(0, 0.010)
    plt.title(" PageRank score with x : alpha = "+str(a1)+" and y : alpha = "+str(a2))
    plt.savefig("ScoreInAlpha"+str(a1)+"_"+str(a2)+".png")
    
    plt.show()
    del p1
    del x
    del y

def kplusPetit(D,k):
    sorted_by_value = sorted(D.items(), key=lambda kv: kv[1])
    i = 0
    res = list()
    for i in range(k):
        res.append(sorted_by_value[i])
    del sorted_by_value
    return res

def kplusGrand(D,k):
    sorted_by_value = sorted(D.items(), key=lambda kv: kv[1],reverse = True)
    i = 0
    res = list()
    for i in range(k):
        res.append(sorted_by_value[i])
    del sorted_by_value
    return res


#p = PageRank("/Vrac/CPA-PageRank/alr21--dirLinks--enwiki-20071018.txt")
#p = PageRank("test.txt")
#p.computation(15)

#som = 0
#for k in p.P.keys():
#    som += p.P[k]
#
#print(som)
#print(kplusPetit(p.P,5))
#[(12588429, 8.029414407102666e-08), (141140, 8.029414407102666e-08), (8612315, 8.029414407102666e-08), (12899417, 8.029414407102666e-08), (12899501, 8.029414407102666e-08)]
#print(kplusGrand(p.P,5))
#[(3434750, 0.003641641771341633), (31717, 0.001595610280130652), (11867, 0.001387173142026925), (36164, 0.0013607089814780002), (5843419, 0.0013295272513515564)]
#p.plotDegOut()
#p.plotDegIn()
#p.clean()

#plotAlpha(0.15,0.1,"/Vrac/CPA-PageRank/alr21--dirLinks--enwiki-20071018.txt",12)
#plotAlpha(0.15,0.2,"/Vrac/CPA-PageRank/alr21--dirLinks--enwiki-20071018.txt",12)
#plotAlpha(0.15,0.5,"/Vrac/CPA-PageRank/alr21--dirLinks--enwiki-20071018.txt",12)
#plotAlpha(0.15,0.9,"/Vrac/CPA-PageRank/alr21--dirLinks--enwiki-20071018.txt",12)

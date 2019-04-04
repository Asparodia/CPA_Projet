

class MinHeap:
    def __init__(self):
        self.heapList = [(0,-1)]
        self.currentSize = 0
        
    def percUp(self,i):
        while i // 2 > 0 :
          if self.heapList[i][1] < self.heapList[i // 2][1]:  
             tmp = self.heapList[i // 2]
             self.heapList[i // 2] = self.heapList[i]
             self.heapList[i] = tmp
             
          i = i // 2
    def percUp2(self,i,tab):
        while i // 2 > 0:
          if self.heapList[i][1] < self.heapList[i // 2][1]:
             #print("percUp",i,i//2)
             tmp = self.heapList[i // 2]
             self.heapList[i // 2] = self.heapList[i]
             self.heapList[i] = tmp

             tab[self.heapList[i // 2][0]] = (i//2)
             tab[self.heapList[i][0]] = i
             
          i = i // 2
          

    def percDown(self,i):
        while (i * 2) <= self.currentSize:
            mc = self.minChild(i)
            if self.heapList[i][1] > self.heapList[mc][1]:
                tmp = self.heapList[i]
                self.heapList[i] = self.heapList[mc]
                self.heapList[mc] = tmp
            i = mc
    def percDown2(self,i,tab):
        while (i * 2) <= self.currentSize:
            mc = self.minChild(i)
            if self.heapList[i][1] > self.heapList[mc][1]:
                #print("percDown",i,mc)
                tmp = self.heapList[i]
                self.heapList[i] = self.heapList[mc]
                self.heapList[mc] = tmp
                
                tab[self.heapList[i][0]] = i
                tab[self.heapList[mc][0]] = mc
                
            i = mc

    def insert(self,k):
        self.heapList.append(k)
        self.currentSize = self.currentSize + 1
        self.percUp(self.currentSize)
        
    def minChild(self,i):
        if i * 2 + 1 > self.currentSize:
            return i * 2
        else:
            if self.heapList[i*2][1] < self.heapList[i*2+1][1]:
                return i * 2
            else:
                return i * 2 + 1
    
    def delMin(self):
        self.heapList[1] = self.heapList[self.currentSize]
        self.currentSize = self.currentSize - 1
        self.heapList.pop()
        self.percDown(1)
    
    def delMin2(self,tab):
        
        tab[self.heapList[1][0]] = -1
        
        retval = self.heapList[1]
        self.heapList[1] = self.heapList[self.currentSize]
        self.currentSize = self.currentSize - 1
        
        self.heapList.pop()

        self.percDown2(1,tab)
        
        return retval
    


    def __repr__(self):
        s =""
        for i in self.heapList[1:]:
            s+=str(i)+" "
        return s
    

            

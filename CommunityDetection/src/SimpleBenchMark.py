import random

import matplotlib.pyplot as plt
import networkx as nx


class SimpleBenchMark:

    def __init__(self,maxNode):
        G = nx.Graph()

        p = 0.8
        q = 0.1

        fichier = open("exo1Graph_P_"+str(p)+"_Q_"+str(q)+".txt", "w")

        for i in range(0, maxNode):
            for j in range(i + 1, maxNode):
                if i // 100 == j // 100:
                    if random.random() < p:
                        G.add_edge(i, j)
                        fichier.write(str(i) + "\t" + str(j) + "\n")
                elif random.random() < q:
                    G.add_edge(i, j)
                    fichier.write(str(i) + "\t" + str(j) + "\n")

        nx.draw(G)
        plt.title("Simple graph with P : "+str(p)+" and Q : "+str(q))
        plt.savefig("exo1Graph_P_"+str(p)+"_Q_"+str(q)+".png")
        plt.show()

SimpleBenchMark(400)
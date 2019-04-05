import matplotlib.pyplot as plt
import networkx as nx

def edgeArray(fileName):
    f = open(fileName, "r")
    edges = list()
    for line in f:
        if(line[0]=="#"):
           continue
        edge=line[:-1].split()
        edges.append((int(edge[0]),int(edge[1])))
    f.close()
    return edges

def graph_reader(input_path):
    """
    methode pour lire un fichier de "input_path" et renvoie un graph
    :param input_path:          fichier à lire.
    :return graph:              Networkx graph, graphe a renvoyer.
    """
    
    edges = edgeArray(input_path)
    graph = nx.from_edgelist(edges)
    return graph


def plot_graph(graph, labels=None):
    dict_community = {}

    for k, v in labels.items():
        dict_community[v] = [k] if v not in dict_community.keys() \
            else dict_community[v] + [k]

    pos = nx.spring_layout(graph)  # positions for all nodes

    color = ['green', 'blue', 'red', 'yellow', 'orange', 'magenta',
             'cyan', 'chocolate', 'pink' ]

    i = 0
    for k, v in dict_community.items():
        while i >= len(color):
            i -= 1
        nx.draw_networkx_nodes(graph,
                               pos,
                               nodelist=v,
                               node_color=color[i],
                               node_size=50,
                               alpha=0.8)
        i += 1
    
    del dict_community
    
    nx.draw_networkx_edges(graph, pos, width=1.0, alpha=0.5)
    
    # Pour avoir les labels sur les node du plot mais c'est moins visible
#    dict_labels = {}
#    dict_labels = {node: node for node, label in labels.items()}
#
#    #nx.draw_networkx_labels(graph, pos)

    plt.axis('off')
    plt.savefig("comunity.png")  # save as png
    # nx.draw(graph)
    plt.show()

from plot_read_data import graph_reader, plot_graph
from LabelPropagation import LabelPropagation

file = "com-youtube.ungraph.txt"
file_test = "test0.txt"
test = "exo1Plot/exo1Graph_P_0.8_Q_0.002.txt"
NB_LOOP = 1000


def run():
    graph = graph_reader(file)
    label_propagation = LabelPropagation(graph)
    label_propagation.propagation()
    print("-------------")
    label_propagation.loop_propagation(NB_LOOP)


if __name__ == "__main__":
    run()

#Propagation num : 96, avec 13799 nombre de communauté.
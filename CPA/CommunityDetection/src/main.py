from plot_read_data import graph_reader, plot_graph
from LabelPropagation import LabelPropagation

file = r"../res/com-youtube.ungraph.txt"
file_test = r"../res/test0.txt"
NB_LOOP = 10


def run():
    graph = graph_reader(file)
    print("Starting label prop")
    label_propagation = LabelPropagation(graph)
    print("-------------")
    #start_time = time.time()
    label_propagation.loop_propagation(NB_LOOP)
    #print("PY Temps d execution : %s secondes ---" % (time.time() - start_time))
    labels = label_propagation.get_labels()
    plot_graph(graph, labels=labels)


if __name__ == "__main__":
    run()

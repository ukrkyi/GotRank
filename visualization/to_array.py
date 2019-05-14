import matplotlib.pyplot as plt
import networkx as nx
import numpy as np


def to_arr(path):
    mtr = None
    with open(path, 'r') as matrix:
        mtr = matrix.readlines()
        mtr = mtr[1:]
        mtr = list(map(lambda x: list(map(lambda x: int(x), x.split())), mtr))
    return mtr


def to_vertex_lst(matrix):
    lst = []
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j]:
                lst.append((i + 1, j + 1, matrix[i][j]))

    return lst


def vertex_lst_to_names(lst):
    names = []
    with open('names.txt', 'r') as names_txt:
        names = names_txt.readlines()
        names = list(map(lambda x: x.strip(), names))
    lst = list(map(lambda x: (names[x[0] - 1], names[x[1] - 1], x[2]), lst))
    return lst


vl = to_vertex_lst(to_arr("matrix.txt"))
vl = vertex_lst_to_names(vl)
print(vl)
graph = nx.MultiDiGraph(directed=True)

options = {
    'node_size': 1000,
    'plot-width': 1900,
    'plot-ehight': 1900

}
graph.add_weighted_edges_from(vl)

pos = nx.spring_layout(graph, k=0.3*1/np.sqrt(len(graph.nodes())), iterations=20)
# pos = nx.graphwiz_layout(graph)
nx.draw_networkx(graph, pos=pos, arrows=True, node_size=1200, node_color='lightblue',
                 linewidths=0.01, font_size=5, font_weight='bold', with_labels=True, dpi=10000000000)

plt.savefig('a.png')
plt.show()

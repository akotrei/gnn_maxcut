import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import networkx as nx

from core.utils import (
    to_binary,
    qubo_matrix,
    graph_regular_k_generate,
    graph_make_random_weight,
)


def show_graph_with_labels(adjacency, labels, bits, legend):
    color_map = []
    for node in bits:
        if node == 1:
            color_map.append("blue")
        else:
            color_map.append("green")

    np.fill_diagonal(adjacency, 0)
    G = nx.from_numpy_matrix(adjacency, create_using=nx.DiGraph)
    layout = nx.spring_layout(G)
    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw(G, layout, node_color=color_map, labels=labels)
    nx.draw_networkx_edge_labels(G, pos=layout, edge_labels=edge_labels)

    extra = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor="none", linewidth=4)
    plt.legend(
        [
            extra,
        ],
        (f"max_cut_value is {legend}",),
        prop={"size": 20},
    )
    plt.show()


def find_max_cut(adjacency: np.array):
    """Find max-cut partition using a brute force approach and one CPU core, 2^N complexity, where N - nodes count"""
    shape = adjacency.shape
    if (len(shape) != 2) or (shape[0] != shape[1]):
        raise ValueError("adjacency matrix should have a squre shape")

    n, _ = shape
    adjacency = qubo_matrix(adjacency)

    max_cut_val = 0
    max_cut_bits = None
    for i in range(2**n):
        bits = to_binary(i, n - 1)
        bits = np.array(bits)
        current_cat = -bits @ adjacency @ bits
        if max_cut_val < current_cat:
            max_cut_val = current_cat
            max_cut_bits = bits

    return max_cut_val, max_cut_bits


if __name__ == "__main__":
    N = 5
    K = 2
    adjacency = graph_regular_k_generate(N, K)
    adjacency = graph_make_random_weight(adjacency)

    max_cut_val, max_cut_bits = find_max_cut(adjacency)

    show_graph_with_labels(
        adjacency, {i: i for i in range(len(adjacency))}, max_cut_bits, str(max_cut_val)
    )

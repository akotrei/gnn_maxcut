import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import networkx as nx


def to_binary(val: int, bits: int):
    """Generate an list of bits that represrnt an unsigned inger @val that occupies @bits in memory"""
    bits = [val >> i & 1 for i in range(bits, -1, -1)]
    return bits


def qubo_matrix(adjacency: np.array):
    """generate from an adjacency matrix @adjacency a matrix for quadratic optimization:
    (see max-cut part of https://arxiv.org/pdf/2107.01188.pdf)
    """

    adjacency = adjacency.copy()
    d = adjacency.sum(axis=1)
    np.fill_diagonal(adjacency, -d)
    return adjacency


def check_symmetric(a, rtol=1e-05, atol=1e-08):
    """Check if a matrix @a is symmetric"""

    return np.allclose(a, a.T, rtol=rtol, atol=atol)


def graph_regular_k_generate(n, k):
    """Generate an regular graph of order k
    TODO imrove via (for example) https://sci-hub.wf/10.1016/j.procs.2020.03.403"""

    assert (
        n > k
    ), "number of nodes neighbours should be strictly less than number of nodes."
    assert (n > 0) and (k > 0), "n and k should be positive"
    assert n * k % 2 == 0, "n*k should be an even number"

    flag = False
    while flag is False:
        adjacency = np.zeros((n, n))
        for i in range(n):
            ones = adjacency.sum(axis=1)
            index = [j for j in range(n) if (j != i) and (ones[j] < k)]
            additional_ones = k - int(ones[i])

            neighbours = np.zeros((len(index),))
            neighbours[:additional_ones] = 1
            np.random.shuffle(neighbours)

            adjacency[i, index] = neighbours
            adjacency[index, i] = neighbours

        s = np.allclose(adjacency.sum(axis=1), k)
        if (s is True) and (check_symmetric(adjacency) is True):
            flag = True

    return adjacency


def graph_make_random_weight(adjacency):
    """Generate from {0, 1} adjacency matrix @adjacency a
    matrix with with weight from 0 to 1 with uniform distribution"""
    rand = np.random.rand(*adjacency.shape)
    adjacency *= rand
    adjacency = (adjacency + adjacency.T) / 2
    return adjacency


def show_graph_with_labels(adjacency, labels, bits, legend=None):
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
    if legend is not None:
        plt.legend(
            [
                extra,
            ],
            (f"max_cut_value is {legend}",),
            prop={"size": 20},
        )
    plt.show()


if __name__ == "__main__":
    N = 40
    K = 20

    adjacency = graph_regular_k_generate(N, K)
    adjacency = graph_make_random_weight(adjacency)
    print(adjacency)
    print(adjacency.sum(axis=1))
    print(check_symmetric(adjacency))

    show_graph_with_labels(adjacency, {i: i for i in range(len(adjacency))}, [1 for _ in range(len(adjacency))])

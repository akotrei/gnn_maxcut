import numpy as np

from core.utils import (
    to_binary,
    qubo_matrix,
    graph_regular_k_generate,
    graph_make_random_weight,
    show_graph_with_labels,
)


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

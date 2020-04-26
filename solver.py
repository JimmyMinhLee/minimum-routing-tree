import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_network, average_pairwise_distance
from userutils import *
import time
import sys, os


def solve(graph):
    """
    Args:
        G: networkx.Graph

    Returns:
        T: networkx.Graph
    """

    # TODO: your code here!
    # return mst_with_pruning(G)
    mst = get_mst(graph)
    pruned_mst = prune(mst)
    pruned_mst_cost = average_pairwise_distance(pruned_mst)

    domset = better_domset_approx(graph)
    if len(domset.nodes()) == 1:
        return domset

    # Dominating Set Initial Solutions
    domset_mstmove = DomSetMSTMove(domset, graph)
    domset_normal = DomSet(domset, graph)

    annealers = [domset_mstmove, domset_normal]
    trees = [pruned_mst]

    for annealer in annealers:
        schedule = annealer.auto(minutes=.5)
        annealer.set_schedule(schedule)
        tree, energy = annealer.anneal()
        trees.append(tree)

    best_tree = pruned_mst
    best_weight = pruned_mst_cost

    for tree in trees:
        if average_pairwise_distance(tree) < best_tree:
            best_tree = tree
            best_tree_weight = average_pairwise_distance(tree)

    return best_tree









# Here's an example of how to run your solver.

# Usage: python3 solver.py test.in

# if __name__ == '__main__':
#     assert len(sys.argv) == 2
#     path = sys.argv[1]
#     G = read_input_file(path)
#     T = solve(G)
#     assert is_valid_network(G, T)
#     print("Average  pairwise distance: {}".format(average_pairwise_distance(T)))
#     write_output_file(T, 'out/test.out')

steps_dict = {

    'large': 5000,
    'medium' : 10000,
    'small' : 20000
}

# Usage: python3 solver.py /inputs
if __name__ == '__main__':

    t0 = time.time()
    assert len(sys.argv) == 2
    input_path = sys.argv[1]
    current_folder = sys.path[0]

    inputs_path = current_folder + input_path
    for input in os.listdir(inputs_path):
        G = read_input_file(inputs_path + '/' + input)
        print("solving: {}".format(input))
        T = solve(G)
        assert is_valid_network(G, T)
        # print("Average  pairwise distance: {}".format(average_pairwise_distance(T)))
        write_output_file(T, 'mst_outputs/{}'.format(input[0:len(input) - 2] + 'out'))
    t1 = time.time()
    print("Elapsed time: {}".format(t1 - t0))

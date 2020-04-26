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

    """
    Annealers:
        MST - random choice in adding an edge and diconnecting an edge
        MSTSmartRandomDisconnect - removes a random edge, adds the minimum across cut
        MSTSmartRandomAdd - removes maximum edge across cut, adds a random edge

        DomSet - removes maximum edge across cut, adds minimum edge across cut
        DomSetMSTMove - removes random edge, adds minimum edge across cut
    """
    mst = get_mst(graph)
    pruned_mst = prune(mst)
    pruned_mst_cost = average_pairwise_distance(pruned_mst)
    print("Pruned MST cost: {}".format(pruned_mst_cost))

    domset = better_domset_approx(graph)
    if len(domset.nodes()) == 1:
        return domset

    # Run annealers on MST graphs
    pruned_mst1 = MST(pruned_mst, graph)
    pruned_mst2 = MSTSmartRandomAdd(pruned_mst, graph)
    pruned_mst3 = MSTSmartRandomDisconnect(pruned_mst, graph)

    # Run annealers on DomSet graphs
    domset_1 = MST(domset, graph)
    domset_2 = MSTSmartRandomAdd(domset, graph)
    domset_3 = MSTSmartRandomDisconnect(domset, graph)

    annealers = [pruned_mst1, pruned_mst2, pruned_mst3, domset_1, domset_2, domset_3]

    best_tree = pruned_mst
    best_tree_weight = pruned_mst_cost

    solution_trees = []
    for annealer in annealers:
        # print(annealer)
        annealer.steps = 1000
        tree, energy = annealer.anneal()
        print()
        print("Resulting solution cost: {}".format(energy))
        solution_trees.append(tree)

    for tree in solution_trees:
        if average_pairwise_distance(tree) < best_tree_weight:
            best_tree = tree
            best_tree_weight = average_pairwise_distance(tree)

    print("Best tree found of cost: {}".format(best_tree_weight))
    return tree












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

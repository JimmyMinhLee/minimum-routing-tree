import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_network, average_pairwise_distance, average_pairwise_distance_fast
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
    mst = get_mst(graph)
    pruned_mst = prune(mst)
    pruned_mst_cost = average_pairwise_distance(pruned_mst)
    print("Pruned MST cost: {}".format(pruned_mst_cost), flush=True)

    domset = better_domset_approx(graph)
    if len(domset.nodes()) == 1:
        print("Found a dominating set of size 0!", flush=True)
        return domset

    domset_1 = RandomMove(domset, graph)
    domset_annealers = [domset_1]
    best_tree = pruned_mst
    best_tree_weight = pruned_mst_cost
    solution_trees = []

    ### FOR ANNEALLING ###
    # annealer = domset_annealers[0]
    # print("performing landscaping of solution space", flush=True)
    # auto_schedule = annealer.auto(minutes=2, steps=2000)
    # print('\n')
    # print("done landscaping, schedule set: {}".format(auto_schedule), flush=True)
    # print('performing annealling on domset initial solutions', flush=True)
    for annealer in domset_annealers:
        for i in range(1):
            # annealer.set_schedule(auto_schedule)
            annealer.Tmax = 5000
            annealer.Tmin = 0.0025
            annealer.steps = 50000
            tree, energy = annealer.anneal()
            ### DEBUGGING ###
            # print('\n')
            # print("Resulting solution cost: {}".format(average_pairwise_distance(tree)), flush=True)
            solution_trees.append(tree)

    for tree in solution_trees:
        if average_pairwise_distance(tree) < best_tree_weight:
            best_tree = tree
            best_tree_weight = average_pairwise_distance(tree)

    # print("Best tree cost: {}".format(average_pairwise_distance_fast(best_tree)))
    pruned_mst_weight = pruned_mst_cost
    print("Pruned MST Cost: {}, Best tree cost: {}".format(pruned_mst_weight, best_tree_weight))
    # print("Tree nodes: {}".format(best_tree.nodes()))
    # print("Tree edges: {}".format(best_tree.edges()))
    print("============")
    print()
    return best_tree

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
    print("solving large inputs", flush=True)
    inputs_path = current_folder + input_path
    for input in os.listdir(inputs_path):
        G = read_input_file(inputs_path + '/' + input)
        print("solving: {}".format(input))
        T = solve(G)
        assert is_valid_network(G, T)
        # print("Final pairwise distance: {}".format(average_pairwise_distance(T)))
        output_folder = "C:\\Users\\jimmy\\desktop\\proj\\outputs\\"
        output_file = input.replace(".in", ".out")
        output_string = output_folder + output_file

        print("Output path: {}".format(output_string))
        print("============")
        print()

        write_output_file(T, output_string)
        os.remove(inputs_path + '/' + input)

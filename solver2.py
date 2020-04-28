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
    print("Pruned MST cost: {}".format(pruned_mst_cost), flush=True)

    domset = better_domset_approx(graph)
    if len(domset.nodes()) == 1:
        print("Found a dominating set of size 0!", flush=True)
        return domset

    # Run annealers on MST graphs
    pruned_mst1 = MST(pruned_mst, graph)
    pruned_mst2 = MSTSmartRandomAdd(pruned_mst, graph)
    pruned_mst3 = MSTSmartRandomDisconnect(pruned_mst, graph)

    # Run annealers on DomSet graphs
    domset_1 = MST(domset, graph)
    domset_2 = MSTSmartRandomAdd(domset, graph)
    domset_3 = MSTSmartRandomDisconnect(domset, graph)

    mst_annealers = [pruned_mst1, pruned_mst2, pruned_mst3]
    domset_annealers = [domset_1]

    best_tree = pruned_mst
    best_tree_weight = pruned_mst_cost

    # Parameters for landscaping - can change to let the solution space explore more
    lscape_minutes = 1

    solution_trees = []

    # for annealer in mst_annealers:
    #     print(annealer, flush=True)
    #     print('performing annealling on mst initial solutions', flush=True)
    #     for i in range(1):
    #         # annealer.set_schedule(auto_schedule)
    #         # annealer.steps = 1000
    #         annealer.steps = 7500
    #         tree, energy = annealer.anneal()
    #         print('\n')
    #         print("Resulting solution cost: {}".format(energy), flush=True)
    #         solution_trees.append(tree)

    annealer = domset_annealers[0]
    print("performing landscaping of solution space", flush=True)
    auto_schedule = {'tmax': 1000.0, 'tmin': 0.025, 'steps': 30000, 'updates': 100}
    print('\n')
    print("done landscaping, schedule set: {}".format(auto_schedule), flush=True)
    print('performing annealling on domset initial solutions', flush=True)
    for annealer in domset_annealers:
        for i in range(1):
            annealer.set_schedule(auto_schedule)
            tree, energy = annealer.anneal()
            print('\n')
            print("Resulting solution cost: {}".format(energy), flush=True)
            solution_trees.append(tree)

    for tree in solution_trees:
        if average_pairwise_distance(tree) < best_tree_weight:
            best_tree = tree
            best_tree_weight = average_pairwise_distance(tree)

    # print("Best tree found of cost: {}".format(best_tree_weight), flush=True)
    pruned_mst_weight = pruned_mst_cost
    print("Pruned MST Cost: {}, Best tree cost: {}".format(pruned_mst_weight, best_tree_weight))
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
    print("solving medium inputs", flush=True)
    inputs_path = current_folder + input_path
    for input in os.listdir(inputs_path):
        if "medium-" in input:
            G = read_input_file(inputs_path + '/' + input)
            print("solving: {}".format(input))
            T = solve(G)
            assert is_valid_network(G, T)
            print("Final pairwise distance: {}".format(average_pairwise_distance(T)))
            output_string = input[0:len(input) - 2] + "out"
            output_string = output_string.replace("input", "output")
            print(output_string, flush=True)
            file_path = "C:/Users/jimmy\desktop/proj/outputs/" + output_string
            write_output_file(T, file_path)
            os.remove(inputs_path + '/' + input)

    t1 = time.time()
    print("Elapsed time: {}".format(t1 - t0))

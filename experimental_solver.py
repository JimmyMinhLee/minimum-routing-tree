import networkx as nx
from parse import read_input_file, write_output_file, read_output_file
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

    We're going to run the graph on a few inputs and compare them.
    """

    ### Initializations ###

    if len(graph.nodes()) == 1:
        return graph

    domset = better_domset_approx(graph)
    domset_cost = average_pairwise_distance_fast(domset)

    if domset_cost == 0:
        print("Found domset of size 0, returning", flush=True)
        return domset

    steiner = steiner_tree(graph)
    unfrozen = nx.Graph(steiner)
    try:
        unfrozen = repeated_pruning(graph, unfrozen)
    except:
        return domset
    steiner_cost = average_pairwise_distance_fast(unfrozen)
    print("Steiner Tree cost: {}".format(steiner_cost), flush=True)
    if is_valid_network(graph, unfrozen):
        return unfrozen
    else:
        return domset


# Usage: python3 solver.py /inputs
if __name__ == '__main__':

    t0 = time.time()
    assert len(sys.argv) == 2
    input_path = sys.argv[1]
    current_folder = sys.path[0]
    # print("solving large inputs", flush=True)
    inputs_path = current_folder + input_path
    for input in os.listdir(inputs_path):

        print()
        print("============")
        G = read_input_file(inputs_path + '/' + input)
        print("solving: {}".format(input))
        print()

        T = solve(G)
        assert is_valid_network(G, T)

        # Getting output file
        output_folder = "C:\\Users\\jimmy\\desktop\\proj\\outputs\\"
        output_file = input.replace(".in", ".out")
        output_string = output_folder + output_file
        print("Output path: {}".format(output_string))

        current_output = read_output_file(output_string, G)
        cost_current_output = average_pairwise_distance_fast(current_output)
        tree_cost = average_pairwise_distance_fast(T)

        if tree_cost < cost_current_output:
            print("Tree cost: {}, Current output cost: {}".format(tree_cost, cost_current_output), flush=True)
            print("Cost of solution better than pre-existing solution; overwriting...", flush=True)
            assert is_valid_network(G, T)
            write_output_file(T, output_string)

        print("============")
        print()

        # write_output_file(T, output_string)
        # os.remove(inputs_path + '/' + input)

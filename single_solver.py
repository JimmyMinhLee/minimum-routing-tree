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

    Run a single proposed algorithm and compare costs to the current output
    Idea behind this is that we want to quickly check if an approach is doing better than the other ones in the outputs already
    """

    ### Initializations ###
    if len(graph.nodes()) == 1:
        return graph

    last = find_last(graph, alpha=100)
    last_annealer = RandomMove(last, graph)
    last_annealer.steps = 10000
    tree, energy = last_annealer.anneal()
    print()
    print("Tree cost: {}".format(average_pairwise_distance_fast(tree)), flush=True)
    tree = repeated_pruning(graph, tree)
    print("New cost: {}".format(average_pairwise_distance_fast(tree)), flush=True)
    print()
    return tree




# Usage: python3 solver.py /inputs
if __name__ == '__main__':

    t0 = time.time()
    assert len(sys.argv) == 2
    input_path = sys.argv[1]
    current_folder = sys.path[0]
    print("solving large inputs", flush=True)
    inputs_path = current_folder + input_path

    for input in os.listdir(inputs_path):
        print(input, flush=True)

        print()
        print("============", flush=True)
        G = read_input_file(inputs_path + '/' + input)
        print("solving: {}".format(input), flush=True)
        print()

        T = solve(G)
        tree_cost = average_pairwise_distance_fast(T)


        # Getting output file
        output_folder = "C:\\Users\\jimmy\\desktop\\proj\\outputs\\"
        output_file = input.replace(".in", ".out")
        output_string = output_folder + output_file
        print("Output path: {}".format(output_string))

        current_output = read_output_file(output_string, G)
        cost_current_output = average_pairwise_distance_fast(current_output)

        if tree_cost < cost_current_output:
            print("Tree cost: {}, Current output cost: {}".format(tree_cost, cost_current_output), flush=True)
            print("Cost of solution better than pre-existing solution; overwriting...", flush=True)
            assert is_valid_network(G, T)
            write_output_file(T, output_string)

        print("============", flush=True)
        print()
        os.remove(inputs_path + '/' + input)

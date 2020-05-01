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

    mst = get_mst(graph)
    pruned_mst = prune(graph, mst)
    last = find_last(graph, alpha = 2)
    last_annealer = RandomMove(graph, last)

    domset = better_domset_approx(graph)
    domset_annealer = RandomMove(domset, graph)

    solutions = [pruned_mst]
    annealers = [domset_annealer, last_annealer]

    ### Annealing ###
    for annealer in annealers:
        annealer.steps = 25000
        annealer.Tmax = 1000
        annealer.Tmin = .0025

        print("annealing...", flush=True)
        print()
        tree, energy = annealer.anneal()
        tree = repeated_pruning(graph, tree)

        print("Iteration solution tree cost: {}".format(average_pairwise_distance_fast(tree)))
        print()

        if average_pairwise_distance_fast(tree) == 0:
            print("Found dominating set of size 0, breaking from solution.")
            print()
            return tree
        solutions.append(tree)

    ### Comparing solution costs against each other ###
    best_solution, best_solution_cost = last, average_pairwise_distance_fast(last)
    print("Intial solution cost: {}".format(best_solution_cost), flush=True)
    print()
    for solution in solutions:
        solution_cost = average_pairwise_distance_fast(solution)
        if solution_cost < best_solution_cost:
            best_solution, best_solution_cost = solution, solution_cost
    print("Final solution cost: {}".format(best_solution_cost), flush=True)
    print()
    return best_solution




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
        os.remove(inputs_path + '/' + input)

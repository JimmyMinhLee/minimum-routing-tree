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

    We're going to run the graph on a few inputs and compare them.
    """

    ### Initializations ###
    mst = get_mst(graph)
    pruned_mst = prune(graph, mst)
    last = find_last(graph, alpha = 2)
    domset = better_domset_approx(graph)
    domset_annealer = RandomMove(domset, graph)
    last_annealer = RandomMove(last, graph)
    solutions = [pruned_mst]
    annealers = [domset_annealer, last_annealer]

    ### Annealing ###
    for annealer in annealers:
        annealer.steps = 50000
        annealer.Tmax = 1000
        annealer.Tmin = .0025

        print("annealing...", flush=True)
        print()
        tree, energy = annealer.anneal()
        tree = repeated_pruning(graph, tree)

        print("Iteration solution tree cost: {}".format(average_pairwise_distance_fast(tree)))
        solutions.append(tree)

    ### Comparing solution costs against each other ###
    best_solution, best_solution_cost = pruned_mst, average_pairwise_distance_fast(pruned_mst)
    print("Intial solution cost: {}".format(best_solution_cost), flush=True)
    for solution in solutions:
        solution_cost = average_pairwise_distance_fast(solution)
        if solution_cost < best_solution_cost:
            best_solution, best_solution_cost = solution, solution_cost

    print("Final solution cost: {}".format(best_solution_cost), flush=True)
    return best_solution




# Usage: python3 solver.py /inputs
if __name__ == '__main__':

    t0 = time.time()
    assert len(sys.argv) == 2
    input_path = sys.argv[1]
    current_folder = sys.path[0]
    print("solving large inputs", flush=True)
    inputs_path = current_folder + input_path
    for input in os.listdir(inputs_path):
        print()
        print("============")
        G = read_input_file(inputs_path + '/' + input)
        print("solving: {}".format(input))
        T = solve(G)
        assert is_valid_network(G, T)

        # Getting output file
        output_folder = "C:\\Users\\jimmy\\desktop\\proj\\outputs\\"
        output_file = input.replace(".in", ".out")
        output_string = output_folder + output_file
        print("Output path: {}".format(output_string))

        current_output = read_input_file(output_folder + output_file)
        current_output_cost = average_pairwise_distance_fast(current_output)

        print("Current outpust cost: {}".format(current_output_cost))

        if average_pairwise_distance_fast(T) < current_output_cost:
            print("Solution cost better than output cost. Rewriting...")
            write_output_file(T, output_string)
        print("============")
        print()
        os.remove(inputs_path + '/' + input)

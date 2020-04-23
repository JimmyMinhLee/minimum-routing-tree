import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_network, average_pairwise_distance
from solver import *
from userutil import *
import sys, os, random



### Run local testing ###

# Example: looks at the MST for the 30'th inputs. #
# batch = get_sml_input(random.randint(0, 100))
# batch = get_sml_input(30)
#
#
# graphs = []
# for input in batch:
#     graph = read_input_file(input)
#     graphs.append(graph)
#
# for graph in graphs:
#     # This line will usually be: tree = algorithm(graph)
#     tree = get_mst(graph)
#     print("Average pairwise distance in MST: {}".format(average_pairwise_distance(tree)))
#
#ç
#     print("Average pairwise distance in MST with pruning: {}".format(average_pairwise_distance(our_tree)))
#     print(is_valid_network(graph, our_tree))

rand_input = get_rand_small()

for input in rand_input:
    graph = read_input_file(input)

    tree = get_mst(graph)
    print("Average pairwise distance in MST: {}".format(average_pairwise_distance(tree)))

    solver = PairwiseDistanceTreeMST(tree, graph)
    tree, energy = solver.anneal()

    # Original settings for annealer
    # Tmax = 25000.0  # Max (starting) temperature
    # Tmin = 2.5      # Min (ending) temperature
    # steps = 50000   # Number of iterations
    # updates = 100   # Number of updates (by default an update prints to stdout)

    solver.Tmax = 10000.0
    solver.Tmin = 0.0
    solver.steps = 100
    solver.updates = 100
    print(tree)
    print("Average pairwise distance in solution: {}".format(average_pairwise_distance(tree)))

import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_network, average_pairwise_distance
from solver import *
from userutils import *
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

rand_input = [get_rand_medium() for i in range(1)]
# rand_input = [get_minput(111)]
print(rand_input)
# medium 111 causes problems
# print(rand_input)
for input in rand_input:
    graph = read_input_file(input)
    # print("Graph nodes: {}".format(graph.nodes()))
    mst = get_mst(graph)

    print("Original cost: {}".format(average_pairwise_distance(mst)))
    mst_prune = MSTSmartRandomDisconnect(mst, graph)
    mst_prune.steps = 5000
    tree, energy = mst_prune.anneal()
    print("Final cost: {}".format(average_pairwise_distance(tree)))

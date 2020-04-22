import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_network, average_pairwise_distance
from solver import *
from userutil import *
import sys, os, random



### Run local testing ###

# Example: looks at the MST for the 30'th inputs. #
# batch = get_sml_input(random.randint(0, 100))
batch = get_sml_input(30)


graphs = []
for input in batch:
    graph = read_input_file(input)
    graphs.append(graph)

for graph in graphs:
    # This line will usually be: tree = algorithm(graph)
    tree = get_MST(graph)
    print("Average pairwise distance in MST: {}".format(average_pairwise_distance(tree)))
    our_tree = mst_with_pruning(graph)
    print("Average pairwise distance in MST with pruning: {}".format(average_pairwise_distance(our_tree)))
    print(is_valid_network(graph, our_tree))

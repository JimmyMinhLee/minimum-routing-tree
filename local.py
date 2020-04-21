import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_network, average_pairwise_distance
from solver import *
from userutil import *
import sys, os, random



### Run local testing ###

# Example: looks at the MST for the 30'th inputs. #
batch = get_sml_input(30)

graphs = []
for input in batch:
    graph = read_input_file(input)
    graphs.append(graph)

for graph in graphs:
    # This line will usually be: tree = algorithm(graph)
    tree = get_MST(graph)
    print("Average pairwise distance: {}".format(average_pairwise_distance(tree)))

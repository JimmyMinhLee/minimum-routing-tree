import networkx as nx
from parse import read_input_file, write_output_file, read_output_file
from utils import is_valid_network, average_pairwise_distance
from solver import *
from userutils import *
import sys, os, random


rand_input = get_linput(1)
graph = read_input_file(rand_input)
steiner = steiner_tree(graph)

copy = nx.Graph(steiner)
validity = is_valid_network(graph, copy)
print(validity)
copy = repeated_pruning(graph, copy)
validity = is_valid_network(graph, copy)
print(validity)

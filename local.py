import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_network, average_pairwise_distance
from solver import *
from userutils import *
import sys, os, random

rand_input = get_rand_large()

graph = read_input_file(rand_input)

mst = get_mst(graph)
pruned_mst = prune(mst)

print(average_pairwise_distance(pruned_mst))
domset = better_domset_approx(graph)
print(average_pairwise_distance(domset))

# Dominating Set Initial Solutions
domset_mstmove = MST(domset, graph)
domset_mstmove.steps = 5000
tree, energy = domset_mstmove.anneal()
print()
print(energy)

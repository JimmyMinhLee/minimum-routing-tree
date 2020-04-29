import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_network, average_pairwise_distance
from solver import *
from userutils import *
import sys, os, random

rand_input = get_sinput(1)

graph = read_input_file(rand_input)
mst = get_mst(graph)
pruned_mst = prune(mst)

domset = better_domset_approx(graph)
print(average_pairwise_distance(pruned_mst))
print(average_pairwise_distance(domset))


domset_mstmove = RandomMove(domset, graph)

# auto_schedule = domset_mstmove.auto(minutes=2, steps=2000)
# domset_mstmove.set_schedule(auto_schedule)
domset_mstmove.steps=100000

print('annealing', flush=True)
print()
tree, energy = domset_mstmove.anneal()
input = rand_input
print(average_pairwise_distance(tree))

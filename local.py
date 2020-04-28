import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_network, average_pairwise_distance
from solver import *
from userutils import *
import sys, os, random

rand_input = get_sinput(100)

graph = read_input_file(rand_input)

mst = get_mst(graph)
pruned_mst = prune(mst)

print(average_pairwise_distance(pruned_mst))
domset = better_domset_approx(graph)
print(average_pairwise_distance(domset))

print("large" in rand_input, flush=True)
# Dominating Set Initial Solutions
domset_mstmove = MST(domset, graph)
# domset_mstmove.steps = 1000
print('landscaping', flush=True)
auto_schedule = domset_mstmove.auto(minutes=.1)
print()
print('annealing', flush=True)
print('auto schdule', auto_schedule)
domset_mstmove.set_schedule(auto_schedule)
tree, energy = domset_mstmove.anneal()
print()
print(energy, flush=True)

input = rand_input

output_string = rand_input[0:len(rand_input) - 2] + "out"
output_string = output_string.replace("input", "output")
print(output_string, flush=True)
write_output_file(tree, output_string)

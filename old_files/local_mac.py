import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_network, average_pairwise_distance
from solver import *
from userutils import *
import sys, os, random
import copy

rand_input = get_sinput(100)

graph = read_input_file(rand_input)

mst = get_mst(graph)
pruned_mst = prune(graph, mst)
last = find_last(graph, alpha = 1.0001)

print(average_pairwise_distance_fast(pruned_mst))
domset = better_domset_approx(graph)
domset = RandomMovePruning(domset, graph)
last = RandomMove(last, graph)

domset.steps=10000
domset.Tmax = 550
domset.Tmin = .0025

last.steps=10000
last.Tmax = 550
last.Tmin = .0025


print('annealing', flush=True)
print()
tree1, energy = domset.anneal()
print("No pruning: {}".format(average_pairwise_distance_fast(tree1)))
tree1 = repeated_pruning(graph, tree1)
print("Pruned: {}".format(average_pairwise_distance_fast(tree1)))

tree2, energy = last.anneal()
print("Tree2: {}".format(average_pairwise_distance_fast(tree2)))
tree2 = repeated_pruning(graph, tree2)
print("Pruned: {}".format(average_pairwise_distance_fast(tree2)))

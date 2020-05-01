import networkx as nx
from parse import read_input_file, write_output_file, read_output_file
from utils import is_valid_network, average_pairwise_distance
from solver import *
from userutils import *
import sys, os, random

rand_input = get_sinput(100)
graph = read_input_file(rand_input)

domset = better_domset_approx(graph)
domset_annealer = RandomMove(domset, graph)
domset_annealer.steps = 25000
tree, energy = domset_annealer.anneal()
print()
print("cost: {}".format(average_pairwise_distance_fast(tree)))
tree = repeated_pruning(graph, tree)
print("cost: {}".format(average_pairwise_distance_fast(tree)))

last = find_last(graph, alpha= 100)
last_annealer = RandomAdd(last, graph)
last_annealer.steps = 25000
tree2, energy = last_annealer.anneal()
print()
print("cost: {}".format(average_pairwise_distance_fast(tree2)))
tree2 = repeated_pruning(graph, tree2)
print("cost: {}".format(average_pairwise_distance_fast(tree2)))


output_file = rand_input.replace(".in", ".out").replace("input", "output")
current_output = read_output_file(output_file, graph)
current_output_cost = average_pairwise_distance_fast(current_output)

if average_pairwise_distance_fast(tree) < current_output_cost:
    print("Previous cost: {}, new cost: {}".format(current_output_cost, average_pairwise_distance_fast(tree)))
    print('overwriting')
    assert is_valid_network(graph, tree)
    write_output_file(tree, output_file)

if average_pairwise_distance_fast(tree2) < current_output_cost:
    print("Previous cost: {}, new cost: {}".format(current_output_cost, average_pairwise_distance_fast(tree2)))
    print('overwriting')
    assert is_valid_network(graph, tree2)

    write_output_file(tree2, output_file)

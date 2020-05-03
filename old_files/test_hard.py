import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_network, average_pairwise_distance
from solver import *
from userutils import *
import sys, os, random
from func_timeout import func_timeout


hard_inputs = [get_linput(3), get_linput(13), get_linput(32), get_linput(107), get_linput(125), get_minput(107)]
not_hard = [get_minput(101), get_linput(101), get_minput(103), get_linput(104)]
print("hard inputs")
for input in hard_inputs:

    graph = read_input_file(input)
    pruned_mst = prune(get_mst(graph))
    nodes = graph.nodes()
    edges = graph.edges()
    domset = better_domset_approx(graph)
    domset_nodes = domset.nodes()
    domset_edges = domset.edges()
    print("original", len(nodes), len(edges))
    print("domset", len(domset_nodes), len(domset_edges), average_pairwise_distance(domset))
print()
print("not hard inputs")

for input in not_hard:
    graph = read_input_file(input)
    pruned_mst = prune(get_mst(graph))
    nodes = graph.nodes()
    edges = graph.edges()
    domset = better_domset_approx(graph)
    domset_nodes = domset.nodes()
    domset_edges = domset.edges()
    print("original", len(nodes), len(edges))
    print("domset", len(domset_nodes), len(domset_edges), average_pairwise_distance(domset))

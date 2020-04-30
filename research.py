from utils import is_valid_network, average_pairwise_distance
import networkx as nx
import sys, os, random
from copy import deepcopy
from simanneal import Annealer
from networkx.algorithms.approximation import dominating_set
import random as rand
from userutils import *
from itertools import *

# Research paper algorithms

### Section: LAST ###
"""
Paper: https://arxiv.org/pdf/cs/0205045.pdf

Psuedocode - as presented in LAST algorithm:
    find_last():
        intialize()
        dfs(r)
        return T: = {(v, p[v]) | v in V - {r}}

    dfs(u):
        if d[u] > alpha * D_{t_s}(r, u):
            add_path(u)
        for each child v of u in T_m:
            relax(u, v)
            dfs(v)
            relax(v, u)

    initialize():
        for each non-root:
            p[non-root] = v
            d[v] = infinity
        d[r] = 0

    add_path(v):
        if d[v] > D_{t_s}(r, v):
            add_path(parent_{t_s}(v))
            relax(parent_{t_s}(v))

    relax(u, v):
        if d[v] > d[u] + w[u, v]
            d[v] = d[u] + w[u, v]
            p[v] = u

"""

def find_last(graph, alpha):
    assert alpha > 1

    root = 1
    mst, parent_mst = get_mst(graph), get_mst_parents(get_mst(graph))
    spt, parent_spt = get_spt(graph)

    def initialize():
        parent, dist = [None] * (len(graph.nodes()) + 1), [float('infinity')] * (len(graph.nodes()) + 1)
        dist[root] = 0
        return parent, dist

    def relax(u, v):
        if dist[v] > dist[u] + get_edge_weight(graph, u, v):
            dist[v] = dist[u] + get_edge_weight(graph,u ,v)
            parent[v] = u

    def dfs(u):
        if dist[u] > alpha * get_distance(graph, root, u):
            add_path(u)
        for child in get_children(parent_mst, u):
            relax(u, child)
            dfs(child)
            relax(child, u)

    def add_path(v):
        if dist[v] > get_distance(graph, root, v):
            add_path(parent_spt[v])
            relax(parent_spt[v], v)

    parent, dist = initialize()
    dfs(root)

    tree = nx.Graph()
    for node in graph.nodes():
        if node != root:
            tree.add_node(node)
            tree.add_node(parent[node])
            edge_weight = get_edge_weight(graph, parent[node], node)
            tree.add_edge(node, parent[node], weight=edge_weight)
    print(tree.edges(), tree.nodes())
    return tree

# Gets the shortest path distance between two nodes inside a tree.
def get_distance(graph, u, v):
    return nx.algorithms.shortest_paths.generic.shortest_path_length(graph, u, v, weight='weight')


# Constructs the shortest paths tree - returns the spt and the parent vertices
def get_spt(graph):
    root = 1
    paths = nx.algorithms.shortest_paths.weighted.single_source_dijkstra_path(graph, root, weight='weight')
    tree = nx.Graph()
    parent = [None] * (len(graph.nodes()) + 1)
    for end in paths.keys():
        path = paths[end]
        current = root
        for node in path:
            if node == current:
                parent[node] = root
            else:
                tree.add_edge(current, node, weight=get_edge_weight(graph, current, node))
                parent[node] = current
                current = node
    return tree, parent

# Gets the parent array of an MST
def get_mst_parents(mst):
    root = 1
    # Can use SPT algorithm as subroutine - the MST should only have one path from start to end
    spt, parent = get_spt(mst)
    return parent

# Gets the child of a vertex in a tree given a parent array
def get_children(parents, u):
    children = []
    root = 1
    for node in range(len(parents)):
        if parents[node] == u and node != root:
            children.append(node)
    return children


### Section: LART ###
"""
Paper: Constructing Light Spanning Tree w/ Small Rounding Cost

    remove_bad():
        spt = compute_all_shortest_paths(g)
        while bad_edge in spt:
            bad_edge = bad_edge(a, b)
            root = a
            if b is not ancestor(x):
                Y* = T union (x, b) \ (a, b)
                Y** = T union (a, x) \ (x, y)
            else:
                Y* = T union (a, x) \ (a, b)
                Y** = T union (b, x) \ (x, y)

            if C(Y*) < C(Y**):
                Y = Y*
            else:
                Y = Y**

    find_lart():
        Input: a graph: G, a real number, alpha > 1, and an integer 1 <= k <= 6 * alpha - 3
        mst = get_mst(G)
        for each R in V(G) and cardinality R <= k:
            construct G^R
            find MST of G^R
            find SPT of G^R
            run FIND_LAST on G^R
            delete edges of ER from T1
            Find the T0 = MST(G|R) - the induced subgraph of G on the vertices of R
            T = T0 U T1
            return T
"""

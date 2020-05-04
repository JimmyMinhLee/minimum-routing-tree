from utils import is_valid_network, average_pairwise_distance
import networkx as nx
import sys, os, random
from copy import deepcopy
from simanneal import Annealer
from networkx.algorithms.approximation import dominating_set
import random as rand
from userutils import *

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

    Will forgo doing remove_bad and focus on the LART, as this was done as a reduction of the problem
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

def find_lart(graph):
    k = len(graph.nodes())
    alpha = ((k + 3)/6) + 1

    # Step 1: find T_M = MST(G)
    T_m = get_mst(graph)
    # For each subset R in V(G), with |R| <= k, construct a spanning tree
    # and keep the minimum cost one.

    # Need some way to exhaust all of them, for now, we just try
    # one iteration for each subset size

    best_tree, best_tree_cost = None, float('infinity')
    for r in range(10):

        nodes = list(graph.nodes())
        subset = rand.sample(nodes, r)

        # Step 2.1: construct G^R - the initial subset with inital edges, adding one ghost root.
        g_r = construct_gr(graph, subset)

        # Step 2.2: find MST of G^R
        # Step 2.3: find the SPT of G^R rooted at R

        # Both these steps are implicit to our implementation of finding the LAST

        def find_last(graph, alpha):
            assert alpha > 1

            # We constructed gr with the root being -1.
            root = len(g_r.nodes()) + 1
            print(root)
            print(len(g_r.nodes()))
            mst, parent_mst = get_mst(graph), get_mst_parents(get_mst(graph))
            spt, parent_spt = get_spt(graph)
            print(parent_spt)
            def initialize():
                parent, dist = [None] * (len(graph.nodes()) + 2), [float('infinity')] * (len(graph.nodes()) + 2)
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

        # Step 2.4: call algorithm FIND_LAST to find the LAST rooted at r.
        tree_1 = find_last(g_r, alpha = alpha)

        # Step 2.5: remove the edges of E_R from T_1, i.e. the edges of G^R from T_1
        tree_1 = remove_edges(tree_1, list(g_r.edges()))

        # Step 2.6: find T_0 = MST(G|R) where G|R is the induced subgraph on the R vertices.
        tree_0 = get_mst(g_r)

        # Step 2.7: set T = T0 U T1
        tree = union_trees(tree_0, tree_1)

        # Step 2.8: compute C(T)
        cost = average_pairwise_distance_fast(tree)

        if cost < best_tree_cost:
            best_tree, best_tree_cost = tree, cost

    return best_tree


def construct_gr(graph, subset):
    g_r = deepcopy(graph)

    for node in list(g_r.nodes()):
        if node in subset:
            g_r.remove_node(node)

    root_node = len(g_r.nodes()) + 1
    g_r.add_node(root_node)
    for other_node in list(g_r.nodes()):
        if other_node == root_node:
            pass
        else:
            g_r.add_edge(root_node, other_node, weight = 0)
    return g_r

def remove_edges(graph, edges):
    copy_graph = deepcopy(graph)
    for edge in edges:
        if edge in list(copy_graph.edges()):
            copy_graph.remove_edge(edge)
    return copy_graph

def union_trees(t1, t2):
    copy_tree = deepcopy(t1)
    for node in list(t2.nodes()):
        copy_tree.add_node(node)
    for edge in list(t2.edges()):
        copy_tree.add_edge(edge)
    return copy_tree




### Section: LART (MIT) ###

"""

Paper: https://groups.csail.mit.edu/tds/papers/Holzer/holzer2014MRCT.pdf

"""

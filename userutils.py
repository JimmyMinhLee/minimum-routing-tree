from utils import is_valid_network, average_pairwise_distance
import networkx as nx
import sys, os, random
from copy import deepcopy
from simanneal import Annealer
import random as rand

def test_function(graph):
    pass
    # Perform a test on whatever you want to run right now



# Annealer that uses MST at first.
class MST(Annealer):
    def __init__(self, state, graph):
        self.state = state
        self.graph = graph
        self.iter = 0
        initial_c = average_pairwise_distance(self.state)
        # self.cost_scalar = 1 / initial_c
        self.cost_scalar = 1
        super(PairwiseDistanceTreeMST, self).__init__(state)  # important!

    def move(self):
        disconnecting_edge = choose_random_edge(self.state.edges())
        u, v = disconnecting_edge[0], disconnecting_edge[1]
        self.state.remove_edge(u, v)
        u_cc = nx.node_connected_component(self.state, u)
        v_cc = nx.node_connected_component(self.state, v)
        connecting_edges = find_connecting_edges(self.graph, u_cc, v_cc)
        random_connecting_edge = choose_random_edge(connecting_edges)
        rce_edge_weight = get_edge_weight(self.graph, u, v)
        u, v = random_connecting_edge[0], random_connecting_edge[1]
        self.state.add_edge(u, v, weight=rce_edge_weight)

    def energy(self):
        return self.cost_scalar * average_pairwise_distance(self.state)

# Random edges
class MSTPrune(Annealer):
    def __init__(self, state, graph):
        self.state = prune(state)
        self.graph = graph
        self.iter = 0
        initial_c = average_pairwise_distance(self.state)
        self.cost_scalar = 1
        super(MSTPrune, self).__init__(state)  # important!

    def move(self):
        if self.state.nodes() == 1 and is_valid_network(self.state, graph):
            return 0
        disconnecting_edge = choose_random_edge(self.state.edges())
        if disconnecting_edge == None:
            return
        u, v = disconnecting_edge[0], disconnecting_edge[1]
        self.state.remove_edge(u, v)
        u_cc = nx.node_connected_component(self.state, u)
        v_cc = nx.node_connected_component(self.state, v)
        connecting_edges = find_connecting_edges(self.graph, u_cc, v_cc)
        if len(connecting_edges) == 0:
            self.state.add_edge(u, v, get_edge_weight(self.state, u, v))
            return
        else:
            random_connecting_edge = choose_random_edge(connecting_edges)
            rce_edge_weight = get_edge_weight(self.graph, u, v)
            u, v = random_connecting_edge[0], random_connecting_edge[1]
            self.state.add_edge(u, v, weight=rce_edge_weight)

    def energy(self):
        return self.cost_scalar * average_pairwise_distance(self.state)

# Starting with MST, disconnects a random edge, adds the minimum across cut
class MSTSmartRandomDisconnect(Annealer):
    def __init__(self, state, graph):
        self.state = prune(state)
        print(average_pairwise_distance(self.state))
        self.graph = graph
        self.iter = 0
        self.cost_scalar = 1
        super(MSTSmartRandomDisconnect, self).__init__(state)  # important!

    def move(self):
        if self.state.nodes() == 1 and is_valid_network(self.state, graph):
            return 0
        disconnecting_edge = choose_random_edge(self.state.edges())
        if disconnecting_edge == None:
            return
        u, v = disconnecting_edge[0], disconnecting_edge[1]
        self.state.remove_edge(u, v)

        u_cc = nx.node_connected_component(self.state, u)
        v_cc = nx.node_connected_component(self.state, v)
        connecting_edges = find_connecting_edges(self.graph, u_cc, v_cc)

        if len(connecting_edges) == 0:
            self.state.add_edge(u, v, min_edge_weight)
            return
        else:
            min_edge, min_edge_weight = minimum_edge_across_cut(self.graph, u_cc, v_cc)
            u, v = min_edge[0], min_edge[1]
            self.state.add_edge(u, v, weight=min_edge_weight)

    def energy(self):
        return average_pairwise_distance(self.state)

# Start with the SPT on the dominating set
class DomSet(Annealer):
    def __init__(self, state, graph):
        self.state = state
        self.graph = graph
        super(DomSet, self).__init__(state)

    def move(self):
        pass

    def cost(self):
        return average_pairwise_distance(self.state)

# Section: Helper Functions

def construct_domsetSPT(graph):
    tree = nx.Graph()
    domset = list(nx.dominating_set(graph))
    starter_node = domset[0]
    tree.add_node(starter_node)
    dist, shortest_paths = nx.single_source_dijkstra(graph, starter_node)
    print(shortest_paths)

# Gets the maximum edge in a graph.
def get_max_edge(graph):
    max_edge = None
    max_edge_weight = 0
    for edge in graph.edges():
        if max_edge == None:
            max_edge = edge
            max_edge_weight = get_edge_weight(graph, edge[0], edge[1])
        if max_edge_weight < get_edge_weight(graph, edge[0], edge[1]):
            max_edge = edge
            max_edge_weight = get_edge_weight(graph, edge[0], edge[1])
    return max_edge

# Partitions the graph into two sets.
def partition_graph(graph):
    copy_nodes = []
    for node in graph.nodes():
        copy_nodes.append(node)
    random.shuffle(copy_nodes)
    midway = int(len(copy_nodes) / 2)
    end = int(len(copy_nodes))
    set1 = copy_nodes[0 : midway]
    set2 = copy_nodes[midway : end]
    return set1, set2

# Chooses the maximum edge across a cut.
def maximum_edge_across_cut(graph, set1, set2):
    cross_edges = find_connecting_edges(graph, set1, set2)
    best_edge = None
    best_edge_weight = 0
    for edge in cross_edges:
        u, v = edge[0], edge[1]
        if best_edge == None:
            best_edge = edge
            best_edge_weight = get_edge_weight(graph, u, v)
        edge_weight = get_edge_weight(graph, edge[0], edge[1])
        if edge_weight > best_edge_weight:
            best_edge = edge
    return best_edge, best_edge_weight

# Chooses the minimum edge across a cut.
def minimum_edge_across_cut(graph, set1, set2):
    cross_edges = find_connecting_edges(graph, set1, set2)
    best_edge = None
    best_edge_weight = 0
    for edge in cross_edges:
        u, v = edge[0], edge[1]
        if best_edge == None:
            best_edge = edge
            best_edge_weight = get_edge_weight(graph, u, v)
        edge_weight = get_edge_weight(graph, edge[0], edge[1])
        if edge_weight < best_edge_weight:
            best_edge = edge
    return best_edge, best_edge_weight

# Choose random edge.
def choose_random_edge(edge_list):
    edge_list = list(edge_list)
    possible_choices = len(edge_list) - 1
    # print(possible_choices)
    if possible_choices < 0 or edge_list == []:
        return None
    return edge_list[rand.randint(0, possible_choices)]

# Gets a random node from the graph.
def get_random_node(graph):
    # O(n)
    list_nodes = list(graph.nodes())
    return choose_random(list_nodes)

# Gets the edges of a node.
def get_edges(graph, node):
    return graph.edges(node)

# Returns edge weight between u and v.
def get_edge_weight(graph, u, v):
    # O(1)
    edge_weight = graph.get_edge_data(u, v)['weight']
    return edge_weight

# Choose random element
def choose_random(list):
    return random.choice(list)

# Finds the remaining nodes not in the graph.
def find_remaining_nodes(tree, graph):
    # O(n log(n))
    tree_nodes = set(tree.nodes())
    graph_nodes = set(graph.nodes())
    return list(graph_nodes - tree_nodes)


# Finds all leaves in a graph.
def find_leaves(graph):
    # O(n)
    leaves = []
    for node in G.nodes():
        if len(G.edges(node)) == 1:
            leaves.append(node)
    return leaves

# Get the MST of the graph.
def get_mst(graph):
    return nx.minimum_spanning_tree(graph)

# Finds an edge between two connected components.
def find_connecting_edges(graph, cc1, cc2):
    connecting_edges = []
    for node in cc1:
        edges = get_edges(graph, node)
        for edge in edges:
            if edge[1] in cc2:
                connecting_edges.append(edge)
    return connecting_edges


# Finds an edge between a vertex and another connected component.
def find_edge(graph, u, cc):
    edges = get_edges(graph, u)
    connecting_edges = []
    for edge in edges:
        if edge[1] in cc:
            connecting_edges.append(edge)
    return connecting_edges

# Get the small, medium and large input files that are numbered: n.
def get_sml_input(n):
    input_folder_path = sys.path[0] + '/inputs'
    num = random.randint(1, 100)
    return [
    input_folder_path + '/small-' + str(n) + '.in',
    input_folder_path + '/medium-' + str(n) + '.in',
    input_folder_path + '/large-' + str(n) + '.in'
]

def get_sinput(n):
    input_folder_path = sys.path[0] + '/inputs'
    num = n
    return input_folder_path + '/small-' + str(num) + '.in'

def get_minput(n):
    input_folder_path = sys.path[0] + '/inputs'
    num = n
    return input_folder_path + '/medium-' + str(num) + '.in'

def get_linput(n):
    input_folder_path = sys.path[0] + '/inputs'
    num = n
    return input_folder_path + '/large-' + str(num) + '.in'


# Get a random small input file.
def get_rand_small():
    input_folder_path = sys.path[0] + '/inputs'
    num = random.randint(1, 100)
    return input_folder_path + '/small-' + str(num) + '.in'


# Get a random medium input.
def get_rand_medium():
    input_folder_path = sys.path[0] + '/inputs'
    num = random.randint(1, 100)
    return input_folder_path + '/medium-' + str(num) + '.in'


# Get a random large input.
def get_rand_large():
    input_folder_path = sys.path[0] + '/inputs'
    num = random.randint(1, 100)
    return input_folder_path + '/large-' + str(num) + '.in'

# Get all the leaves in our graph.
def find_leaves(G):
    leaves = []
    for node in G.nodes():
        if len(G.edges(node)) == 1:
            leaves.append(node)
    return leaves

# Prune the leaves of our tree according to some cost function.
def prune(tree):
    leaves = find_leaves(tree)
    if len(leaves) == 1:
        return tree
    original_cost = average_pairwise_distance(tree)
    for node in leaves:
        edges = list(get_edges(tree, node))
        if len(tree.nodes()) == 1:
            return tree
        if len(edges) == 1:
            edge = edges[0]
            copy_tree = deepcopy(tree)
            u, v = edge[0], edge[1]
            copy_tree.remove_node(node)
            new_cost = average_pairwise_distance(copy_tree)
            if new_cost < original_cost:
                tree.remove_node(node)
                original_cost = new_cost
        else:
            pass

    return tree

def our_min_domset(G, weight=None):
    if len(G) == 0:
        return set()
    dom_set = set()
    dom_tree = nx.Graph()
    def _cost(node_and_neighborhood):
        v, neighborhood = node_and_neighborhood
        return G.nodes[v].get(weight, 1) / len(neighborhood - dom_set)

    vertices = set(G)
    neighborhoods = {v: {v} | set(G[v]) for v in G}

    while vertices:
        dom_node, min_set = min(neighborhoods.items(), key=_cost)
        dom_set.add(dom_node)
        dom_tree.add_node(dom_node)
        del neighborhoods[dom_node]
        vertices -= min_set

    return dom_set

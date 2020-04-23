from utils import is_valid_network, average_pairwise_distance
import networkx as nx
import sys, os, random
from copy import deepcopy
from simanneal import Annealer
import random as rand

"""
We're going to use simulated annealling on our graph
to make it constantly change and check for the best solution.
I think that this does things greedily at first, because the
probability of choosing a better option will always be higher
than if we choose a worse option.

The two primary ideas I have:
    1. Start with an MST. Then, randomly choose a vertex in the graph
    and see if we can add/remove it from the tree in a way that will
    make the cost better.

    2. Start with a single node. Then, randomly choose a vertex in the
    graph and see if it will make the cost better.

Considerations:
    1. What is the state of the algorithm?
    2. How do we want to define movement?
    3. Would it be better to start with just one node in the tree and build
    our graph from there?

### Starting with an MST  ###
    Algorithm:
        1. Start with the MST.
        2. State will be the tree thus far: T = nx.Graph().
        3. Then, "move" will pick an arbitrary vertex in the graph,
        and add it to our state.
        4. We want to stop when T is a valid_network of the graph G.

    How to define move?
        1. We want the algorithm to construct a valid network of the graph.
        2. Given that a node is already in the network, we want to see if
        removing it could be accomplished while retaining the validity of
        the graph.
            a. Using copy.deep_copy to track the states of both
            may be too costly, so we'll need to find a better way of
            doing this.
        3. If the node is not in the network, we want to see if
        adding the node will improve the cost of our MST - this should be easy.


    Considerations:
        1. This doesn't account for being able to remove nodes, but I think
        for simplicity's sake we can start by just randomly adding nodes into
        the tree. Once we get that T is a valid network, we stop.

    Potential Optimizations:
        1. Use some pruning algorithm after we construct the T to remove
        nodes from the graph wherever possible.

    Log: April 23
        1. Start with the MST.
        2. Prune initially.
        3. Then, re-arrange edges inside of the tree.
        4. Maybe prune again?
"""

# Annealer that uses MST at first.
class PairwiseDistanceTreeMST(Annealer):
    def __init__(self, state, graph):
        self.state = state
        self.graph = graph
        self.iter = 0
        super(PairwiseDistanceTreeMST, self).__init__(state)  # important!

    def move(self):
        # IF ERROR WITH EDGE, MAKE SURE YOU INDEX TO 1!
        # Used later
        initial_energy = self.energy()

        # Perform algorithm:
            # 1. Disconnect and use a different edge in the graph.
            # 2. If this disconnects the components, reconnect them.

        # 1.
        disconnecting_edge = choose_random_edge(self.state.edges())
        # print("Disconnecting edge: {}".format(disconnecting_edge))
        # Endpoints of edge we'll disconnect:
        u, v = disconnecting_edge[0], disconnecting_edge[1]
        self.state.remove_edge(u, v)

        # O(V + E); they run DFS on each vertex.
        u_cc = nx.node_connected_component(self.state, u)
        v_cc = nx.node_connected_component(self.state, v)
        # print("Connected components: {}, {}".format(u_cc, v_cc))

        # O(E^2); have to potentially check every node in each connected component
        connecting_edges = find_connecting_edges(self.graph, u_cc, v_cc)
        # print(connecting_edges)

        # Pick a random connecting edge and add it to the tree.
        random_connecting_edge = choose_random_edge(connecting_edges)
        rce_edge_weight = get_edge_weight(self.graph, u, v)
        u, v = random_connecting_edge[0], random_connecting_edge[1]
        # print(random_connecting_edge)
        self.state.add_edge(u, v, weight=rce_edge_weight)
        return -1 * (initial_energy - self.energy())


    def energy(self):
        return average_pairwise_distance(self.state)

# Annealer that uses one node at first.
class PairwiseDistanceTreeNode(Annealer):
    def __init__(self, state, G):
        pass

    def move(self):
        initial_energy = self.energy()
        return self.energy() - initial_energy

    def energy(self):
        return average_pairwise_distance(self.state)

# Section: Helper Functions

# Choose random edge.
def choose_random_edge(edge_list):
    edge_list = list(edge_list)
    possible_choices = len(edge_list) - 1
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

# Get a random small input file.
def get_rand_small():
    input_folder_path = sys.path[0] + '/inputs'
    num = random.randint(1, 100)
    return [
    input_folder_path + '/small-' + str(num) + '.in',
]

# Get a random medium input.
def get_rand_medium():
    input_folder_path = sys.path[0] + '/inputs'
    num = random.randint(1, 100)
    return [
    input_folder_path + '/medium-' + str(num) + '.in',
]

# Get a random large input.
def get_rand_large():
    input_folder_path = sys.path[0] + '/inputs'
    num = random.randint(1, 100)
    return [
    input_folder_path + '/large-' + str(num) + '.in'
]

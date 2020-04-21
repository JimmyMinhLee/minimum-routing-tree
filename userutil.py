from utils import is_valid_network, average_pairwise_distance
import networkx as nx
import grinpy as gp
import networkx.algorithms.approximation.dominating_set as dom
import sys, os, random


### SECTION: GENERATE RANDOM INPUT ###

# Picks 10 random numbers and creates list of small, medium and large inputs corresponding to the numbers generated.
def create_input_lists():
    input_folder_path = sys.path[0] + '/inputs'

    # Gets us 10 random numbers
    random_numbers = [random.randrange(0, 100) for i in range(10)]

    large_inputs = []
    med_inputs = []
    small_inputs = []
    for num in random_numbers:
        file_name = input_folder_path + '/{}-' + str(num) + '.in'
        large_inputs.append(file_name.format('large'))
        med_inputs.append(file_name.format('medium'))
        small_inputs.append(file_name.format('small'))
    return large_inputs, med_inputs, small_inputs

# Get the small, medium and large input files that are numbered: n.
def get_sml_input(n):
    input_folder_path = sys.path[0] + '/inputs'
    num = random.randint(0, 100)
    return [
    input_folder_path + '/small-' + str(n) + '.in',
    input_folder_path + '/medium-' + str(n) + '.in',
    input_folder_path + '/large-' + str(n) + '.in'
]

# Get a random small, medium and large input file.
def get_rand():
    input_folder_path = sys.path[0] + '/inputs'
    num = random.randint(0, 100)
    return [
    input_folder_path + '/small-' + str(num) + '.in',
    input_folder_path + '/medium-' + str(num) + '.in',
    input_folder_path + '/large-' + str(num) + '.in'
]
### SECTION: ALGORITHMS ###

tree = nx.Graph()

def domset_approx(G, T):
    t_set = min_weighted_dominating_set(G)
    for u in t_set:
        edges = G.edges(u)
        for edge in edges:
            v = edge[1]
            weight = G.get_edge_data(u, v)['weight']
            if v in t_set:
                T.add_edge(u, v, weight=weight)
    return T

def edge_domset_approx(G, T):
    t_set = min_edge_dominating_set(G)
    for edge in t_set:
        print("Edge:{}".format(edge))
    return T




### SECTION: ALGORITHM UTILITIES ###
def get_MST(G):
    return nx.minimum_spanning_tree(G)

def get_most_connected_vertex(G):
    best_vertex = None
    for node in G.nodes():
        if best_vertex == None:
            best_vertex = node
        if len(list(nx.all_neighbors(G, node))) > len(list(nx.all_neighbors(G, best_vertex))):
            best_vertex = node
    return best_vertex

def get_neighbors(G, node):
    return list(nx.all_neighbors(G, node))

def get_most_connected_neighbor(G, node):
    best_neighbor = None
    for neighbor in nx.all_neighbors(G, node):
        if best_neighbor == None:
            best_neighbor = neighbor
        if len(list(nx.all_neighbors(G, neighbor))) > len(list(nx.all_neighbors(G, best_neighbor))):
            best_neighbor = neighbor
    return best_neighbor

def get_best_vertex(G):
    best_vertex = get_most_connected_vertex(G)
    while len(G.edges(best_vertex)) == 0:
        if best_vertex == None:
            return
        G.remove_node(best_vertex)
        best_vertex = get_most_connected_vertex(G)
    return best_vertex

# Ripped from source code #
def min_weighted_dominating_set(G, weight=None):
    r"""Returns a dominating set that approximates the minimum weight node
    dominating set.

    Parameters
    ----------
    G : NetworkX graph
        Undirected graph.

    weight : string
        The node attribute storing the weight of an node. If provided,
        the node attribute with this key must be a number for each
        node. If not provided, each node is assumed to have weight one.

    Returns
    -------
    min_weight_dominating_set : set
        A set of nodes, the sum of whose weights is no more than `(\log
        w(V)) w(V^*)`, where `w(V)` denotes the sum of the weights of
        each node in the graph and `w(V^*)` denotes the sum of the
        weights of each node in the minimum weight dominating set.

    Notes
    -----
    This algorithm computes an approximate minimum weighted dominating
    set for the graph `G`. The returned solution has weight `(\log
    w(V)) w(V^*)`, where `w(V)` denotes the sum of the weights of each
    node in the graph and `w(V^*)` denotes the sum of the weights of
    each node in the minimum weight dominating set for the graph.

    This implementation of the algorithm runs in $O(m)$ time, where $m$
    is the number of edges in the graph.

    References
    ----------
    .. [1] Vazirani, Vijay V.
           *Approximation Algorithms*.
           Springer Science & Business Media, 2001.

    """
    # The unique dominating set for the null graph is the empty set.
    if len(G) == 0:
        return set()

    # This is the dominating set that will eventually be returned.
    dom_set = set()

    def _cost(node_and_neighborhood):
        """Returns the cost-effectiveness of greedily choosing the given
        node.

        `node_and_neighborhood` is a two-tuple comprising a node and its
        closed neighborhood.

        """
        v, neighborhood = node_and_neighborhood
        return G.nodes[v].get(weight, 1) / len(neighborhood - dom_set)

    # This is a set of all vertices not already covered by the
    # dominating set.
    vertices = set(G)
    # This is a dictionary mapping each node to the closed neighborhood
    # of that node.
    neighborhoods = {v: {v} | set(G[v]) for v in G}

    # Continue until all vertices are adjacent to some node in the
    # dominating set.
    while vertices:
        # Find the most cost-effective node to add, along with its
        # closed neighborhood.
        dom_node, min_set = min(neighborhoods.items(), key=_cost)
        # Add the node to the dominating set and reduce the remaining
        # set of nodes to cover.
        dom_set.add(dom_node)
        del neighborhoods[dom_node]
        vertices -= min_set

    return dom_set

# Ripped from source code #
def min_edge_dominating_set(G):
    r"""Returns minimum cardinality edge dominating set.

    Parameters
    ----------
    G : NetworkX graph
      Undirected graph

    Returns
    -------
    min_edge_dominating_set : set
      Returns a set of dominating edges whose size is no more than 2 * OPT.

    Notes
    -----
    The algorithm computes an approximate solution to the edge dominating set
    problem. The result is no more than 2 * OPT in terms of size of the set.
    Runtime of the algorithm is $O(|E|)$.
    """
    if not G:
        raise ValueError("Expected non-empty NetworkX graph!")
    return nx.maximal_matching(G)

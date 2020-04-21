from userutil import *
import copy



def create_G():
    G = nx.Graph()
    G.add_edge(1, 2, weight = 5)
    G.add_edge(2, 6, weight = 1)
    G.add_edge(1, 3, weight = 4)
    G.add_edge(1, 4, weight = 2)
    G.add_edge(3, 4, weight = 1)
    G.add_edge(3, 5, weight = 4)
    return G

def test_most_connected():
    node = get_most_connected_vertex(G)
    print("Expected: 1, Actual: {}".format(node))

def test_best_neighbor():
    node = get_most_connected_neighbor(G, 1)
    print("Expected: 3, Actual: {}".format(node))

def test_get_edge_data():
    edge_data = G.get_edge_data(1, 2)
    print(edge_data)

def test_domset_neighbors():
    T = nx.Graph()
    G = create_G()
    print("MST cost: {}".format(average_pairwise_distance(get_MST(G))))
    T = domset_neighbors_alg(G, T)
    print("T is valid network: {}".format(is_valid_network(create_G(), T)))
    print("T's cost: {}".format(average_pairwise_distance(T)))
    print(T.edges())
    print(T.nodes())


def test_remove_node():
    T = nx.Graph()
    best_vertex = get_most_connected_vertex(G)
    T.add_node(best_vertex)
    best_neighbor = get_most_connected_neighbor(G, best_vertex)
    edge = G.get_edge_data(best_vertex, best_neighbor)
    edge_weight = edge['weight']
    T.add_edge(best_vertex, best_neighbor, weight=edge_weight)
    G.remove_node(best_vertex)


# test_most_connected()
# test_best_neighbor()
# test_get_edge_data()
test_domset_neighbors()
# test_remove_node()

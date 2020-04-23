from userutil import *
def create_G():
    G = nx.Graph()
    G.add_edge(1, 2, weight = 5)
    G.add_edge(2, 6, weight = 1)
    G.add_edge(1, 3, weight = 4)
    G.add_edge(3, 4, weight = 1)
    G.add_edge(1, 4, weight = 1)
    G.add_edge(3, 5, weight = 4)
    G.to_undirected()
    return G

def test_get_rand_node():
    G = create_G()
    node = get_random_node(G)
    print(node)

def test_get_edges():
    G = create_G()
    node = get_random_node(G)
    edges = get_edges(G, node)
    print(edges)

def test_choose_random_edge():
    G = create_G()
    node = get_random_node(G)
    edges = get_edges(G, node)
    random_edge = choose_random_edge(edges)
    print(random_edge)

def test_get_edge_weight():
    G = create_G()
    node = get_random_node(G)
    edges = get_edges(G, node)
    random_edge = choose_random_edge(edges)
    edge_weight = get_edge_weight(G, node, random_edge[1])
    print(edge_weight)

def test_move_MST():
    G = create_G()
    mst = get_mst(G)

    print("All nodes: {}".format(mst.nodes()))

    random_node = get_random_node(G)
    edges = get_edges(G, random_node)
    print("Edges to node: {}; {}".format(random_node, edges))
    # Must always index to [1] to find the other edge.
    # Perform algorithm
    random_node = get_random_node(G)
    print("Random node: {}".format(random_node))
    edges = get_edges(G, random_node)

    # if this random node is a leaf to the tree, route it somewhere else.
    if len(edges) == 1:
        pass

    # otherwise, reroute while preserving validity.
    random_edge = choose_random_edge(edges)
    connecting_vertex = random_edge[1]

    con_v_cc = nx.node_connected_component(G, connecting_vertex)
    connecting_edges = find_edge(G, random_node, con_v_cc)

    new_edge = choose_random_edge(connecting_edges)
    new_edge_weight = get_edge_weight(G, random_node, new_edge[1])
    new_connecting_vertex = new_edge[1]

    mst.remove_edge(connecting_vertex, random_node)
    mst.add_edge(random_node, new_connecting_vertex, weight = new_edge_weight)


    print("New edges to node: {}; {}".format(random_node, edges))

    print("All nodes: {}".format(mst.nodes()))
    print("Is new graph connected: {}".format(nx.is_connected(mst)))

def test_find_edge():
    g = create_G()
    mst = get_mst(g)

    g.add_edge(10, 1, weight="10")
    print(find_edge(g, 10, mst))
# create_G()
# test_get_rand_node()
# test_get_edges()
# test_choose_random_edge()
# test_get_edge_weight()
test_move_MST()
# test_find_edge()

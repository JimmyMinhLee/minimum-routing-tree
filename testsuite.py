from userutils import *
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

    solver = PairwiseDistanceTreeMST(mst, G)
    solver.move()
    print("Is connected? {}".format(nx.is_connected(solver.state)))

def test_find_edge():
    g = create_G()
    mst = get_mst(g)

    g.add_edge(10, 1, weight="10")
    print(find_edge(g, 10, mst))

def test_prune():
    mst = get_mst(create_G())
    prune(mst)

def test_partition_graph():
    g = create_G()
    print(partition_graph(g))

def test_choose_max_cut_edge():
    g = create_G()
    l, r = partition_graph(g)
    print(maximum_edge_across_cut(g, l, r))

def test_max_edge():
    g = create_G()
    print(get_max_edge(g))

def test_construct_domsetSPT():
    g = create_G()
    print(construct_domsetSPT(g))

def test_domset_approx():
    g = create_G()
    print(domset_approx(g))

def test_better_domset():
    pass
# create_G()
# test_get_rand_node()
# test_get_edges()
# test_choose_random_edge()
# test_get_edge_weight()
# test_move_MST()
# test_find_edge()
# test_prune()
# test_partition_graph()
# test_choose_max_cut_edge()
# test_max_edge()
# test_construct_domsetSPT()
# test_domset_approx()
# test_better_domset()

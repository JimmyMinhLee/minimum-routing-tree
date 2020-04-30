from userutils import *
from research import *

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

def test_last():
    g = create_G()
    print(find_last(g, alpha = 2))

def test_distance():
    g = create_G()
    print(get_distance(g, 1, 6))

def test_spt():
    g = create_G()
    print(get_spt(g))

def test_mst_parents():
    g = create_G()
    print(get_mst_parents(get_mst(g)))

def test_get_children():
    g = create_G()
    mst_parents = get_mst_parents(get_mst(g))
    print(get_children(mst_parents, 1))
    print(get_children(mst_parents, 2))
    print(get_children(mst_parents, 3))

def test_prune():
    g = create_G()
    mst_g = get_mst(g)
    tree = prune(g, mst_g)
    print(average_pairwise_distance_fast(tree))

def test_repeated_prune():
    g = create_G()
    mst_g = get_mst(g)
    tree = repeated_pruning(g, mst_g)
    print(average_pairwise_distance_fast(tree))

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


# test_last()
# test_spt()
# test_distance()
# test_mst_parents()
# test_get_children()

test_prune()

# Can only perform one iteration 
test_repeated_prune()

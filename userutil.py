from utils import is_valid_network, average_pairwise_distance
import networkx as nx
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

###  First algorithm idea:

# 1. Choose a node with the maximum amount of neighbors.
# 2. Add it to our tree.
# 3. Remove this node from the graph.
# 4. Look for all subsequent vertices that has the maximum amount of neighbors.
# 5. Do some calculation on the edges; maybe we'd want to make sure that adding
# this is the best we can do in comparison to all other edges; or even just look
# at which neighbors have the most vertices.
# 6. Add this new vertex to the tree.
# 7. Repeat until the graph is 0.

###

tree = nx.Graph()
def domset_neighbors_alg(G, T):
    if len(list(G.nodes())) == 0:
        return T
    # 1, 2: get the node with the most amount of neighbors and add it to our tree.
    best_vertex = get_most_connected_vertex(G)
    T.add_node(best_vertex)

    # 3: Look for all subsequent vertices that has the maximum amount of neighbors.
    best_neighbor = get_most_connected_neighbor(G, best_vertex)
    # Once we have a vertex that has no more numbers, we want to stop the current iteration.
    if best_neighbor == None:
        return T

    # 4: Add the corresponding edge between the best vertex and best neighbor.
    edge = G.get_edge_data(best_vertex, best_neighbor)
    try:
        edge_weight = edge['weight']
    except:
        print("Caught error at, Vertex: {} Neighbor: {} Edge: {}".format(best_vertex, best_neighbor, edge) )
        return

    # 5: Add this neighbor and edge to the graph.
    T.add_edge(best_vertex, best_neighbor, weight=edge_weight)

    # 6: Remove the best vertex from the graph along with all of its neighbors, besides the best one.
    for neighbor in get_neighbors(G, best_vertex):
        if neighbor != best_neighbor:
            G.remove_node(neighbor)
    G.remove_node(best_vertex)

    # 7: Repeat until the graph has no vertices.
    domset_neighbors_alg(G, T)
    return T






def domset_distance_alg(G):
    pass

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

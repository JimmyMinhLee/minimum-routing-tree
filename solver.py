import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_network, average_pairwise_distance
from userutil import *
import sys, os


def solve(G):
    """
    Args:
        G: networkx.Graph

    Returns:
        T: networkx.Graph
    """

    # TODO: your code here!
    pass




# Here's an example of how to run your solver.

# Usage: python3 solver.py test.in

# if __name__ == '__main__':
#     assert len(sys.argv) == 2
#     path = sys.argv[1]
#     G = read_input_file(path)
#     T = solve(G)
#     assert is_valid_network(G, T)
#     print("Average  pairwise distance: {}".format(average_pairwise_distance(T)))
#     write_output_file(T, 'out/test.out')

if __name__ == '__main__':
    assert len(sys.argv) == 2
    input_path = sys.argv[1]
    current_folder = sys.path[0]

    inputs_path = current_folder + input_path
    for input in os.listdir(inputs_path):
        G = read_input_file(inputs_path + '/' + input)
        T = solve(G)
        assert is_valid_network(G, T)
        # print("Average  pairwise distance: {}".format(average_pairwise_distance(T)))
        write_output_file(T, 'outputs/{}'.format(input[0:len(input) - 2] + 'out'))

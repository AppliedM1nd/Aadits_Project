import pytest
from Project_Code_File4 import dijkstra, Node


def test_dijkstra_all_connected():
    nodes = {}
    expected_distances_dict = {'A':0, 'B':10, 'C':6, 'D':7, 'E':4, 'F':3, 'G':6}
    expected_previous_nodes = {'B':'A', 'C':'E', 'D':'F', 'E':'F', 'F':'A', 'G':'F'}
    for letter in 'ABCDEFG':
        nodes[letter] = Node(letter, 'Network1')
    nodes['A'].add_connection('B', 10)
    nodes['A'].add_connection('F', 3)
    nodes['A'].add_connection('C', 7)
    nodes['F'].add_connection('E', 1)
    nodes['E'].add_connection('C', 2)
    nodes['D'].add_connection('F', 4)
    nodes['D'].add_connection('G', 2)
    nodes['F'].add_connection('G', 3)
    assert dijkstra("A", nodes) == expected_distances_dict, expected_previous_nodes

test_dijkstra_all_connected()

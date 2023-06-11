"""
Author: Ebin Paul
"""

from utils.nexus_parser import get_distance_block
from algorithms.floyd_warshall import get_ultrametric_network_edges

filepath = "C:/Users/ebinp/Downloads/test_nexus/dolphins_binary.nex"

distance_matrix, vertices = get_distance_block(filepath)

ultrametric_network, ultrametric_network_delta = get_ultrametric_network_edges(
    distance_matrix, vertices
)

print(f"{ultrametric_network = }")

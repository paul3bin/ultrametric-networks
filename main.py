"""
AUTHOR: Ebin Paul

"""

import os

from algorithms.floyd_warshall import get_network_edges
from utils.nexus_parser import get_distance_block
from utils.visualizer import VisualiseNetwork

# file_path = input("Enter file path: ")
# file_path = r"C:\Users\ebinp\Downloads\test_nexus\algae.nex"
# file_path = r"C:\Users\ebinp\Downloads\test_nexus\dolphins_binary.nex"
file_path = r"C:\Users\ebinp\Downloads\test_nexus\coronavirus.fasta.nex"
# file_path = r"C:\Users\ebinp\Downloads\test_nexus\rubber.nex"

title = file_path.split("\\")[-1].split(".")[0]

# verifying if file path exists
if os.path.exists(file_path):
    distance_matrix, vertices = get_distance_block(file_path)

    ultrametric_network, ultrametric_network_delta = get_network_edges(
        distance_matrix, vertices
    )

    print(f"{ultrametric_network = }")

    network = VisualiseNetwork(vertices, ultrametric_network, title)

    network.display()

else:
    print("File does not exist!")

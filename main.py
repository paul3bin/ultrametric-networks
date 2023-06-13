"""
Author: Ebin Paul
"""

import matplotlib.pyplot as plt
import networkx as nx
import os

from algorithms.floyd_warshall import get_ultrametric_network_edges
from utils.nexus_parser import get_distance_block

file_path = input("Enter file path: ")

# verifying if file path exists
if os.path.exists(file_path):
    distance_matrix, vertices = get_distance_block(file_path)

    ultrametric_network, ultrametric_network_delta = get_ultrametric_network_edges(
        distance_matrix, vertices
    )

    print(f"{ultrametric_network = }")

    # intitalizing the graph for creating network
    network = nx.Graph()

    # adding nodes/vertices to the graph
    network.add_nodes_from(vertices)

    # adding the edges to graph with weights
    for key in ultrametric_network:
        nodes = key.split(",")
        network.add_edge(nodes[0], nodes[1], weight=ultrametric_network[key])

    # defining the positions of nodes using layout functions
    positions = nx.spring_layout(network)

    # positions = nx.random_layout(network)
    # positions = nx.shell_layout(network)
    # positions = nx.circular_layout(network)
    # positions = nx.planar_layout(network)

    # extracting the edge weights
    edge_weights = nx.get_edge_attributes(network, "weight")

    # plotting the graph
    nx.draw_networkx(
        network,
        positions,
        with_labels=True,
        node_color="lightblue",
        node_size=500,
        font_size=12,
        font_weight="bold",
    )
    nx.draw_networkx_edges(network, positions, width=2)
    nx.draw_networkx_edge_labels(network, positions, edge_labels=edge_weights)

    # displaying the network
    plt.axis("off")
    plt.show()

else:
    print("File does not exist!")

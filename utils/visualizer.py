"""
AUTHOR: Ebin Paul

DESCRIPTION: The given code represents a Python class called VisualiseNetwork that facilitates the visualization 
    and export of an ultrametric network. It uses libraries such as NetworkX, Pyvis, and Plotly to accomplish this. 
    The class takes in information about the network, including the vertices and their connections with associated weights. 
    It provides methods to display the network visualization, export it as an image file, and potentially export it as a PDF file.
    The visualization includes nodes representing the vertices and edges representing the connections between the nodes, 
    with the edge weights displayed as labels. The class offers flexibility in choosing different layout algorithms
    for positioning the nodes in the visualization.

REFERENCES: 
    - https://plotly.com/python/network-graphs/
    - https://pyvis.readthedocs.io/en/latest/tutorial.html#edges
    - https://pyvis.readthedocs.io/en/latest/tutorial.html#networkx-integration
    - https://towardsdatascience.com/pyvis-visualize-interactive-network-graphs-in-python-77e059791f01
    - https://towardsdatascience.com/tutorial-network-visualization-basics-with-networkx-and-plotly-and-a-little-nlp-57c9bbb55bb9
    - https://plotly.com/python/static-image-export/
    - https://community.plotly.com/t/static-image-export-hangs-using-kaleido/61519/4
"""
import os

import networkx as nx
import plotly.graph_objects as go
import pyvis.network as net


class VisualiseNetwork:
    # intialising class variable which is a dictionary
    # with key-value pairs of different layouts
    layout = {
        "random": nx.random_layout,
        "spring": nx.spring_layout,
        "shell": nx.shell_layout,
        "circular": nx.circular_layout,
        "planar": nx.planar_layout,
    }

    def __init__(
        self,
        vertices: list,
        ultrametric_network: dict,
        title: str,
        layout_type: str = "spring",
    ):
        self.vertices = vertices
        self.ultrametric_network = ultrametric_network
        self.title = title

        # intitalizing the graph object for creating network
        self.graph = nx.Graph()

        # adding nodes/vertices to the graph
        self.graph.add_nodes_from(self.vertices)

        # adding the edges to graph with weights
        for key in self.ultrametric_network:
            nodes = key.split(",")
            self.graph.add_edge(
                nodes[0], nodes[1], weight=self.ultrametric_network[key]
            )

        # defining the positions of nodes using layout functions
        self.positions = self.layout[layout_type](self.graph)

    def display(self):
        # initialising a Pyvis network object
        network = net.Network(width="100%", directed=False)

        # adding the nodes and edges to the network object
        network.from_nx(self.graph)

        # enabling the interactive feature of the visualisation
        network.toggle_drag_nodes(True)

        # network.show_buttons(filter_=True)

        # Display the plot
        network.show(f"{self.title}.html", notebook=False)

    def export_to_file(self, file_type: str = "png", dpi: int = 300):
        # extracting the edge weights
        edge_weights = nx.get_edge_attributes(self.graph, "weight")

        # Create lists to store the coordinates and text labels for the edges
        x_edges = []
        y_edges = []
        edge_labels = []

        # Iterate over each edge and add coordinates and labels
        for edge, weight in edge_weights.items():
            x0, y0 = self.positions[edge[0]]
            x1, y1 = self.positions[edge[1]]
            x_edges += [x0, x1, None]
            y_edges += [y0, y1, None]
            edge_labels.append(weight)

        # Create the scatter trace for the edges with labels
        edge_trace = go.Scatter(
            x=x_edges,
            y=y_edges,
            mode="lines+text",
            line=dict(color="rgb(200,200,200)", width=1),
            textfont=dict(color="black", size=12),
            hoverinfo="none",
        )

        # Add edge coordinates to the edge trace
        for edge in self.graph.edges():
            x0, y0 = self.positions[edge[0]]
            x1, y1 = self.positions[edge[1]]
            edge_trace["x"] += tuple([x0, x1, None])
            edge_trace["y"] += tuple([y0, y1, None])

        # Create node trace
        node_trace = go.Scatter(
            x=[],
            y=[],
            text=list(self.graph.nodes()),
            mode="markers+text",
            hoverinfo="text",
            textposition="top center",
            marker=dict(
                color="lightblue",
                size=15,
                line=dict(color="black", width=1),
            ),
        )

        # Add node coordinates to the node trace
        for node in self.graph.nodes():
            x, y = self.positions[node]
            node_trace["x"] += tuple([x])
            node_trace["y"] += tuple([y])

        # Create figure
        fig = go.Figure(data=[edge_trace, node_trace])

        # Customize figure layout
        fig.update_layout(
            title=f"Ultrametric Network - {self.title}",
            title_x=0.5,
            showlegend=False,
            hovermode="closest",
            dragmode="orbit",
            margin=dict(b=20, l=5, r=5, t=40),
            annotations=[
                dict(
                    text="",
                    showarrow=False,
                    xref="paper",
                    yref="paper",
                    x=0.005,
                    y=-0.002,
                    font=dict(size=14),
                )
            ],
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        )

        try:
            if not os.path.exists("output"):
                os.mkdir("output")

            fig.write_image(
                f"output/{self.title}.{file_type}",
                format=file_type,
                width=1200,
                height=800,
                scale=dpi / 72,
            )

        except Exception as e:
            print("Error occured while saving the result to a file.")
            print(str(e))

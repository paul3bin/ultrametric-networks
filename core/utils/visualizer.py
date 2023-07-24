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
import networkx as nx
import plotly.graph_objects as go
import pyvis.network as net


class VisualiseNetwork:
    # intialising class variable which is a dictionary
    # with key-value pairs of different layouts
    layout = {
        "Random": nx.random_layout,
        "Spring": nx.spring_layout,
        "Shell": nx.shell_layout,
        "Circular": nx.circular_layout,
        "Planar": nx.planar_layout,
    }

    def __init__(
        self,
        vertices: list,
        ultrametric_network: dict,
        folder_path: str,
        title: str = "Ultrametric Network",
        layout_type: str = "Spring",
    ):
        """
        Initialize the VisualiseNetwork class.

        Parameters:
            vertices (list): List of vertices/nodes in the ultrametric network.
            ultrametric_network (dict): Dictionary representing the ultrametric network,
                                       with keys as edge tuples and values as edge weights.
            title (str, optional): Title of the network visualization. Default is "Ultrametric Network".
            layout_type (str, optional): Type of layout to use for the network visualization.
                                        Should be one of: "Random", "Spring", "Shell", "Circular", or "Planar".
                                        Default is "Spring".
        Raises:
            ValueError: If either 'vertices' or 'ultrametric_network' is empty or not provided.
        """

        # Validate 'vertices' parameter
        if not vertices:
            raise ValueError("Vertices list cannot be empty.")

        # Validate 'ultrametric_network' parameter
        if not ultrametric_network:
            raise ValueError("Ultrametric network dictionary cannot be empty.")

        self.vertices = vertices
        self.ultrametric_network = ultrametric_network
        self.title = title
        self.folder_path = folder_path

        # intitalizing the graph object for creating network
        self.graph = nx.Graph()

        # adding nodes/vertices to the graph
        self.graph.add_nodes_from(self.vertices)

        # adding the edges to graph with weights
        for key in self.ultrametric_network:
            nodes = key.split(",")
            self.graph.add_edge(
                nodes[0],
                nodes[1],
                weight=self.ultrametric_network[key],
                length=self.ultrametric_network[key],
            )

        # defining the positions of nodes using layout functions
        self.positions = self.layout[layout_type](self.graph)

        self.fig = None

    def display(self, height="600px", width="60%"):
        """
        Create an interactive Pyvis visualization of the ultrametric network and display it in a web browser.

        This method generates an interactive visualization of the ultrametric network using Pyvis,
        and the resulting HTML file is displayed in a web browser. The nodes can be dragged interactively
        in the visualization to explore the network structure.
        """
        # initialising a Pyvis network object
        network = net.Network(
            height="600px",
            width="60%",
            directed=False,
            notebook=False,
            neighborhood_highlight=False,
            select_menu=False,
            filter_menu=False,
            bgcolor="#ffffff",
            font_color=False,
            layout=None,
            # heading=f"Ultrametric Network of {self.title}",
            cdn_resources="local",
        )

        # adding the nodes and edges to the network object
        network.from_nx(self.graph)

        # enabling the interactive feature of the visualisation
        network.toggle_drag_nodes(True)

        network.show_buttons(filter_=["edges"])

        network.toggle_physics(False)

        # Display the plot
        network.show(f"{self.folder_path}/{self.title}.html", notebook=False)

    def build_export_plot(self, layout: str = "Spring"):
        """
        Build a static Plotly figure of the ultrametric network for export or preview.

        Parameters:
            layout (str, optional): Type of layout to use for the network visualization.
                                    Should be one of: "Random", "Spring", "Shell", "Circular", or "Planar".
                                    Default is "Spring".

        Returns:
            plotly.graph_objs.Figure: A static Plotly figure representing the ultrametric network.
        """

        # Check if the provided layout name is in the layout dictionary
        if layout in self.layout:
            layout_function = self.layout[layout]
        else:
            print(
                f"Warning: Unsupported layout '{layout}'. Using default layout 'Spring'."
            )
            layout_function = self.layout[
                "Spring"
            ]  # Use 'Spring' as the default layout

        # extracting the edge weights
        edge_weights = nx.get_edge_attributes(self.graph, "weight")

        # defining the positions of nodes using layout functions
        self.positions = layout_function(self.graph)

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
            # title=f"Ultrametric Network - {self.title}",
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

        self.fig = fig

    def preview_export(self):
        # Display the plot
        self.fig.show()

    def export_to_file(
        self,
        file_path: str = "output.png",
        file_type: str = "png",
        width=1200,
        height=1080,
        dpi: int = 300,
    ):
        """
        Export the static Plotly figure of the ultrametric network to a file.

        Parameters:
            file_path (str, optional): File path where the exported figure should be saved.
                                      Default is "output.png".
            layout (str, optional): Type of layout to use for the network visualization.
                                    Should be one of: "Random", "Spring", "Shell", "Circular", or "Planar".
                                    Default is "Spring".
            file_type (str, optional): File format for the exported figure.
                                      Should be one of the supported formats by Plotly.
                                      Default is "png".
            width (int, optional): Width of the visualisation of the exported image.
                                   Default is 1200
            height (int, optional): Height of the visualisation of the exported image.
                                   Default is 1080
            dpi (int, optional): Dots per inch (resolution) of the exported image.
                                 Default is 300.

            Raises:
                ValueError: If an unsupported file format is provided.
                IOError: If there is an error while saving the figure to the specified file path.
        """
        try:
            self.fig.write_image(
                file_path,
                format=file_type,
                width=width,
                height=height,
                scale=dpi / 72,
            )

        except Exception as e:
            print("Error occured while saving the result to a file.")
            print(str(e))
        except ValueError as ve:
            print(
                f"Error: Unsupported file format '{file_type}'. Please use a supported format."
            )
        except IOError as ioe:
            print(
                f"Error: Unable to save the figure to '{file_path}'. Please check the file path and try again."
            )
            print(f"Original error message: {str(ioe)}")

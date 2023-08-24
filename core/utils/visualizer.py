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
    - https://networkx.org/documentation/stable/tutorial.html
    - https://networkx.org/documentation/stable/tutorial.html#adding-attributes-to-graphs-nodes-and-edges
    - https://pyvis.readthedocs.io/en/latest/tutorial.html#edges
    - https://pyvis.readthedocs.io/en/latest/tutorial.html#networkx-integration
    - https://towardsdatascience.com/pyvis-visualize-interactive-network-graphs-in-python-77e059791f01
    - https://towardsdatascience.com/tutorial-network-visualization-basics-with-networkx-and-plotly-and-a-little-nlp-57c9bbb55bb9
    - https://plotly.com/python/static-image-export/
    - https://community.plotly.com/t/static-image-export-hangs-using-kaleido/61519/4
    - https://community.plotly.com/t/displaying-edge-labels-of-networkx-graph-in-plotly/39113/3
    - https://stackoverflow.com/questions/67273472/is-it-possible-to-display-weight-of-edges-of-a-network-using-pyvis-and-python
    - https://networkx.org/documentation/stable/reference/readwrite/generated/networkx.readwrite.gml.write_gml.html
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
            folder_path (str): Path of parent directory of the Nexus file used for computing network.
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
                title=self.ultrametric_network[key],
            )

        layout_function = self.layout[layout_type]

        # defining the positions of nodes using layout functions
        self.positions = layout_function(self.graph)

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
            width="100%",
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

    def get_edge_trace(self):
        """
        Generate Plotly traces for the edges and their corresponding edge weights.

        Returns:
            tuple: A tuple containing two Plotly traces.
                - The first trace represents the edges in the network.
                - The second trace represents the edge weights as text labels.
        """
        # Create lists to store the coordinates, text labels, and edge weights for the edges
        x_edges = []
        y_edges = []
        edge_labels = []
        edge_weights_labels = []
        xtext = []  # For edge weight text x positions
        ytext = []  # For edge weight text y positions

        # extracting the edge weights
        edge_weights = nx.get_edge_attributes(self.graph, "weight")

        # Iterate over each edge and add coordinates, labels, and weights
        for edge, weight in edge_weights.items():
            x0, y0 = self.positions[edge[0]]
            x1, y1 = self.positions[edge[1]]
            x_edges += [x0, x1, None]
            y_edges += [y0, y1, None]
            edge_labels.append(weight)
            edge_weights_labels.append(f"{weight}")  # Add weight as a text label
            xtext.append((x0 + x1) / 2)  # Calculate x position for edge weight text
            ytext.append((y0 + y1) / 2)  # Calculate y position for edge weight text

        # Create the scatter trace for the edges with labels and weights
        edge_trace = go.Scatter(
            x=x_edges,
            y=y_edges,
            mode="lines",
            line=dict(color="rgb(0,0,0)", width=1),
        )

        # Create the scatter trace for the edge weights as text labels
        eweights_trace = go.Scatter(
            x=xtext,
            y=ytext,
            mode="text",
            marker_size=12,
            text=edge_weights_labels,  # Set the text labels to the edge_weights_labels list
            textposition="top center",
            hovertemplate="%{text}<extra></extra>",
        )

        return edge_trace, eweights_trace

    def get_node_trace(self):
        """
        Generate Plotly trace for the nodes in the ultrametric network.

        Returns:
            plotly.graph_objs.Scatter: A Plotly trace representing the nodes in the network.
        """
        # Create node trace
        node_trace = go.Scatter(
            x=[],
            y=[],
            text=list(self.graph.nodes()),
            mode="markers+text",
            hoverinfo="text",
            textposition="top center",
            marker=dict(
                color="black",  # Set marker color to black
                size=15,
                line=dict(color="black", width=1),
            ),
        )

        return node_trace

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

        # defining the positions of nodes using layout functions
        self.positions = layout_function(self.graph)

        edge_trace, eweights_trace = self.get_edge_trace()

        # Add edge coordinates to the edge trace
        for edge in self.graph.edges():
            x0, y0 = self.positions[edge[0]]
            x1, y1 = self.positions[edge[1]]
            edge_trace["x"] += tuple([x0, x1, None])
            edge_trace["y"] += tuple([y0, y1, None])

        node_trace = self.get_node_trace()

        # Add node coordinates to the node trace
        for node in self.graph.nodes():
            x, y = self.positions[node]
            node_trace["x"] += tuple([x])
            node_trace["y"] += tuple([y])

        # Create figure
        # Create figure
        fig = go.Figure(
            data=[edge_trace, node_trace, eweights_trace],
            layout=go.Layout(
                # title="Ultrametric Network",
                # title_x=0.5,
                showlegend=False,
                hovermode="closest",
                dragmode="orbit",
                margin=dict(b=20, l=5, r=5, t=40),
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            ),
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

    def export_network_to_gml(self, file_path: str):
        """
        Export the NetworkX graph to the XGMML format and save it to the specified file.

        This method takes a NetworkX graph and writes it in the XGMML (eXtensible Graph Markup and Modeling Language)
        format to the provided file path. XGMML is a standardized format used for representing graph structures
        with associated data attributes.

        Parameters:
            file_path (str): The path to the file where the XGMML representation of the graph will be saved.

        Note:
            GML is a flexible format that supports a wide range of graph data. The method uses the NetworkX
            function `nx.readwrite.write_gml()` to write the graph to the GML format.

        Example:
            network = Network()  # Assuming the Network class has been instantiated
            network.export_network_to_xgmml("my_graph.xgmml")
        """

        nx.readwrite.write_gml(self.graph, file_path)

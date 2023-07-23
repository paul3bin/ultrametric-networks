"""
AUTHOR: Ebin Paul

DESCRIPTION: The adapted Floyd-Warshall algorithm computes the largest ultrametric denoted as W∗, 
             which is dominated by an input ultrametric W. W∗ assigns zero distance to self-loops 
             and ensures that the distance between any two vertices is not greater than the maximum 
             distance from either vertex to a third vertex. The algorithm constructs the ultrametric 
             network G(V|W) by finding edges where the distances in W and W∗ are equal. It achieves 
             this efficiently using an adaptation of the Floyd-Warshall all-pairs shortest-path 
             algorithm in O(|V|^3) time. The resulting ultrametric network provides valuable insights 
             into evolutionary relationships and classification.

"""

import copy


def get_network_edges(
    distance_matrix: list,
    vertices: list,
    threshold: int = 0,
) -> tuple:
    """
    Returns a tuple of dictionaries containing the edges of an ultrametric network
    and its delta edges with weights.

    Parameters:
        distance_matrix (list): The distance matrix representing the pairwise distances between vertices.
        vertices (list): The list of vertex labels.
        threshold (int, optional): The threshold value for considering delta edges.
            If provided, only edges with weights within (W_star[i][j] + threshold) of distance_matrix[i][j]
            will be included in the ultrametric_network_delta dictionary. Default is 0.

    Returns:
        tuple: A tuple containing two dictionaries:
            - The ultrametric_network dictionary containing ultrametric edges and their weights.
            - The ultrametric_network_delta dictionary containing delta edges and their weights (if threshold > 0).
    """

    ultrametric_network = {}
    ultrametric_network_delta = {}

    number_of_vertices = len(vertices)

    W_star = compute_distance_matrix(distance_matrix, number_of_vertices)

    for i in range(number_of_vertices):
        for j in range(number_of_vertices):
            if i == j:
                continue

            edge = f"{vertices[i]},{vertices[j]}"
            weight = round(W_star[i][j], 3)

            if W_star[i][j] == distance_matrix[i][j]:
                if edge[::-1] not in ultrametric_network.keys():
                    ultrametric_network[edge] = weight

            if threshold > 0 and (W_star[i][j] + threshold) >= distance_matrix[i][j]:
                if edge[::-1] not in ultrametric_network_delta.keys():
                    ultrametric_network_delta[edge] = weight

        continue

    return ultrametric_network, ultrametric_network_delta


def compute_distance_matrix(distance_matrix: list, number_of_vertices: int) -> list:
    """
    Computes and returns the distance matrix for the ultrametric network
    using an adapted Floyd-Warshall algorithm.

    Parameters:
        distance_matrix (list): The distance matrix representing the pairwise distances between vertices.
        number_of_vertices (int): The number of vertices in the graph.

    Returns:
        list: The resultant distance matrix for the ultrametric network.
    """

    distance_tables = [distance_matrix]

    for k in range(number_of_vertices):
        distance_matrix_k = copy.deepcopy(distance_tables[-1])
        prev_dist_matrix = distance_tables[-1]

        for i in range(number_of_vertices):
            for j in range(number_of_vertices):
                if i == j:
                    continue

                new_distance = min(
                    prev_dist_matrix[i][j],
                    max(prev_dist_matrix[i][k], prev_dist_matrix[k][j]),
                )

                distance_matrix_k[i][j] = new_distance

        # adding the distance table to the list of distance tables
        distance_tables.append(distance_matrix_k)

    W_star = distance_tables[-1]

    return W_star


if __name__ == "__main__":
    test_values = {
        "test_1": {
            "distance_matrix": [
                [0, 3, 5, 2],
                [3, 0, 4, 1],
                [5, 4, 0, 6],
                [2, 1, 6, 0],
            ],
            "vertices": ["U", "V", "W", "X"],
        },
        "test_2": {
            "distance_matrix": [
                [0, 1, 2, 3],
                [1, 0, 3, 2],
                [2, 3, 0, 1],
                [3, 2, 1, 0],
            ],
            "vertices": ["A", "B", "C", "D"],
        },
        "test_3": {
            "distance_matrix": [
                [0, 1, 2, 3, 4],
                [1, 0, 4, 3, 2],
                [2, 4, 0, 1, 3],
                [3, 3, 1, 0, 2],
                [4, 2, 3, 2, 0],
            ],
            "vertices": ["A", "B", "C", "D", "E"],
        },
        "test_4": {
            "distance_matrix": [
                [0, 1, 2, 3, 4, 5],
                [1, 0, 5, 4, 3, 2],
                [2, 5, 0, 1, 4, 3],
                [3, 4, 1, 0, 5, 2],
                [4, 3, 4, 5, 0, 1],
                [5, 2, 3, 2, 1, 0],
            ],
            "vertices": ["A", "B", "C", "D", "E", "F"],
        },
    }

    ultrametric_network, ultrametric_network_delta = get_network_edges(
        test_values["test_3"]["distance_matrix"], test_values["test_3"]["vertices"]
    )

    print(f"{ultrametric_network = }")
    print(f"{ultrametric_network_delta = }")

"""
Author: Ebin Paul

Description: The adapted Floyd-Warshall algorithm computes the largest ultrametric denoted as W∗, 
             which is dominated by an input ultrametric W. W∗ assigns zero distance to self-loops 
             and ensures that the distance between any two vertices is not greater than the maximum 
             distance from either vertex to a third vertex. The algorithm constructs the ultrametric 
             network G(V|W) by finding edges where the distances in W and W∗ are equal. It achieves 
             this efficiently using an adaptation of the Floyd-Warshall all-pairs shortest-path 
             algorithm in O(|V|^3) time. The resulting ultrametric network provides valuable insights 
             into evolutionary relationships and classification.

"""

import copy


def get_ultrametric_network_edges(
    distance_matrix: list,
    vertices: list,
    threshold: int = 0,
) -> tuple:
    """
    returns a tuple of dictionaries which contains the edges of an ultrametric network as keys
    and its weight as its values.
    """

    ultrametric_network = {}
    ultrametric_network_delta = {}

    number_of_vertices = len(vertices)

    W_star = compute_distance_matrix(distance_matrix, number_of_vertices)

    for i in range(number_of_vertices):
        for j in range(number_of_vertices):
            if i == j:
                continue
            if W_star[i][j] == distance_matrix[i][j]:
                if f"{vertices[j]},{vertices[i]}" not in ultrametric_network.keys():
                    ultrametric_network[f"{vertices[i]},{vertices[j]}"] = W_star[i][j]

            if threshold > 0:
                if (W_star[i][j] + threshold) >= distance_matrix[i][j]:
                    if (
                        f"{vertices[j]},{vertices[i]}"
                        not in ultrametric_network_delta.keys()
                    ):
                        ultrametric_network_delta[
                            f"{vertices[i]},{vertices[j]}"
                        ] = W_star[i][j]

        continue

    return ultrametric_network, ultrametric_network_delta


def compute_distance_matrix(distance_matrix: list, number_of_vertices: int) -> list:
    """
    function returns a list which is the resultant distance matrix for the ultrametric network,
    which is obtained after computing the given distance matrix using adapted Floyd-Warshall algorithm.
    """

    distance_tables = [distance_matrix]

    for k in range(number_of_vertices):
        D_k = copy.deepcopy(distance_tables[-1])
        prev_dist_matrix = distance_tables[-1]

        for i in range(number_of_vertices):
            for j in range(number_of_vertices):
                if i == j:
                    continue

                new_distance = min(
                    prev_dist_matrix[i][j],
                    max(prev_dist_matrix[i][k], prev_dist_matrix[k][j]),
                )

                D_k[i][j] = new_distance

        # adding the distance table to the list of distance tables
        distance_tables.append(D_k)

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

    ultrametric_network, ultrametric_network_delta = get_ultrametric_edges(
        test_values["test_3"]["distance_matrix"], test_values["test_3"]["vertices"]
    )

    print(f"{ultrametric_network = }")
    print(f"{ultrametric_network_delta = }")

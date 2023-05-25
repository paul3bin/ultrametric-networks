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


def floyd_warshall_ultrametric_network(distance_matrix: list, vertices: list) -> tuple:
    """
    This function returns a list which is the resultant distance matrix for the ultrametric network,
    which is obtained after computing the given distance matrix using adapted Floyd-Warshall algorithm.
    The function also returns a dictionary that has ultrametrix edge as the key and its weight as value.
    """
    number_of_vertices = len(vertices)
    distance_tables = [distance_matrix]
    ultrametric_network_edges = {}
    network_queue = []

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

    for i in range(number_of_vertices):
        for j in range(number_of_vertices):
            if i == j:
                continue
            if W_star[i][j] == distance_matrix[i][j]:
                if (
                    f"{vertices[j]}, {vertices[i]}"
                    not in ultrametric_network_edges.keys()
                ):
                    ultrametric_network_edges[f"{vertices[i]}, {vertices[j]}"] = W_star[
                        i
                    ][j]

        continue

    return W_star, ultrametric_network_edges


if __name__ == "__main__":
    distance_matrix = [
        [0, 3, 5, 2],
        [3, 0, 4, 1],
        [5, 4, 0, 6],
        [2, 1, 6, 0],
    ]

    vertices = ["U", "V", "W", "X"]

    print(floyd_warshall_ultranet(distance_matrix, vertices))

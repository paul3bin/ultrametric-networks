"""
Author: Ebin Paul
"""

import re


def get_distance_block(filepath: str) -> tuple:
    distance_matrix, vertices = None, None

    with open(filepath, "r") as file:
        nexus_content = file.read()

    # Use regular expressions to extract the distance block
    distance_block_pattern = r"(?i)BEGIN\s+DISTANCES;(.+?)END;"
    distance_block_match = re.search(distance_block_pattern, nexus_content, re.DOTALL)

    if distance_block_match:
        distance_block = distance_block_match.group(1)
        matrix_pattern = r"(?i)MATRIX\n([\s\S]*)(.+?);"
        matrix_match = re.search(matrix_pattern, distance_block, re.DOTALL)

        if matrix_match:
            # splitting the data based on new-line character
            matrix_data = matrix_match.group(1).split("\n")

            distance_matrix = []
            vertices = []
            for data in matrix_data:
                distance_data = list(filter(lambda x: x != "", data.split(" ")[1:]))

                # getting the name of vertex from the list and appending it to the list
                vertex = distance_data.pop(0)
                vertex = vertex.replace("'", "")
                vertices.append(vertex)

                distance_matrix.append([float(x) for x in distance_data])

    else:
        print("Distance block not found.")

    return distance_matrix, vertices

"""
Author: Ebin Paul

Description: This Python script provides a function for parsing the distance block from a Nexus (.nex) file. 
            The Nexus file format is commonly used in phylogenetic analysis to store and exchange data.
            The get_distance_block function takes the filepath of the Nexus file as input and returns a tuple 
            containing the distance matrix and the list of vertices. The script utilizes regular expressions 
            to extract the distance block from the Nexus file, which is typically enclosed between the 
            "BEGIN DISTANCES;" and "END;" tags. Within the distance block, it searches for the "MATRIX" section, 
            which contains the actual distance data. The distance matrix is extracted by splitting the data based 
            on the new-line character and parsing each line. The vertex names are retrieved from the list 
            and appended to the vertices list, while the distance values are converted to floats and stored 
            in the distance_matrix list. If the distance block or matrix is not found within the Nexus file,
            an appropriate message is displayed.
"""

import re


def get_distance_block(file_path: str) -> tuple:
    # initialising the variables for distance matrix and vertices as None
    distance_matrix, vertices = None, None

    # opening the file using the path received in read mode.
    with open(file_path, "r") as file:
        nexus_content = file.read()

    # Use regular expressions to extract the distance block
    distance_block_pattern = r"(?i)BEGIN\s+DISTANCES;(.+?)END;"
    distance_block_match = re.search(distance_block_pattern, nexus_content, re.DOTALL)

    if distance_block_match:
        distance_block = distance_block_match.group(1)

        # Use regular expressions to extract the matrix from distance block
        matrix_pattern = r"(?i)MATRIX\n([\s\S]*)(.+?);"
        matrix_match = re.search(matrix_pattern, distance_block, re.DOTALL)

        # checking if matrix is found from the block
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

                # converting the matrix values from list to float and appending to the list
                distance_matrix.append([float(x) for x in distance_data])

    else:
        print("Distance block not found.")

    return distance_matrix, vertices

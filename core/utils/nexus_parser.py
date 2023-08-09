"""
AUTHOR: Ebin Paul

DESCRIPTION: This Python script provides a function for parsing the distance block from a Nexus (.nex) file. 
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

REFERENCES:
    - https://en.wikipedia.org/wiki/Regular_expression
    - https://docs.python.org/3/library/re.html
    - https://developers.google.com/edu/python/regular-expressions
"""

import re


def get_distance_block(file_path: str) -> tuple:
    """
    Extracts the distance matrix and vertices from a Nexus file containing a distance block.

    The function reads the contents of the Nexus file specified by `file_path`, extracts the distance
    block using regular expressions, and then parses the distance matrix and vertices from the block.

    Parameters:
        file_path (str): The path to the Nexus file containing the distance block.

    Returns:
        tuple: A tuple containing two elements - the distance matrix as a list of lists (2D list) of floats,
               and the vertices as a list of strings. The first element contains the distances between the
               vertices, and the second element contains the names of the vertices.

    Raises:
        Exception: If the distance block is not found in the Nexus file.
        ValueError: If there is an issue converting the distance values to float.

    Note:
        The Nexus file must have a distance block in the following format:

        BEGIN DISTANCES;
        MATRIX
          <distance data>
        ;
        END;

        where <distance data> represents the distance matrix in the Nexus file.
    """

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
                try:
                    distance_values = [float(x) for x in distance_data]
                except ValueError:
                    raise ValueError("Error converting distance values to float.")

                distance_matrix.append(distance_values)

            return distance_matrix, vertices

    print("Distance block not found.")
    return None, None

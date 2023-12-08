# Import necessary libraries
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt


def generate_graph(file) -> nx.graph.Graph:
    # Open and read the maze file
    maze_file = open(file, "r")
    text_maze = maze_file.read()

    # Split the maze into lines
    text_lines = text_maze.splitlines()

    # Initialize a graph for the maze
    maze_graph = nx.Graph()

    # Loop through each character in each line of the maze
    for i, line in enumerate(text_lines):
        for j, char in enumerate(line):
            # If the character is a start, end, or path node, add it to the graph
            if char in ["S", "E", "O"]:
                maze_graph.add_node((i // 2, j // 2))
                # If the node above the current node is a path, add an edge
                if i > 0 and text_lines[i - 1][j] == " ":
                    maze_graph.add_edge((i // 2, j // 2), (i // 2 - 1, j // 2))
                # If the node to the left of the current node is a path, add an edge
                if j > 0 and text_lines[i][j - 1] == " ":
                    maze_graph.add_edge((i // 2, j // 2), (i // 2, j // 2 - 1))

    return maze_graph


def show_graph(graph: nx.graph.Graph):
    # Get the maximum y-coordinate to invert the y-coordinates
    max_y = max(y for x, y in graph.nodes())

    # Define the positions of the nodes in the graph
    pos = {node: (node[1], max_y - node[0]) for node in graph.nodes()}

    # Draw the graph with labels and bold font
    nx.draw(graph, pos, with_labels=True, font_weight="bold")

    # Display the graph
    plt.show()

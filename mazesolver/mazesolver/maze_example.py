edges_list = [
    ("S", 2),
    (1, 2),
    (1, 4),
    (3, 6),
    (4, 7),
    (5, 2),
    (5, 6),
    (6, 9),
    (7, 8),
    (8, "E"),
]

import networkx as nx

maze_graph = nx.Graph()
maze_graph.add_edges_from(edges_list)

print(maze_graph)

import heapq
import networkx as nx
from maze_gen.graph_gen import generate_graph

# Example using an adjacency list for the graph
# representation as dict-of-dicts

# graph = {
#     'A': {'B': 2, 'C': 1},
#     'B': {'A': 2, 'C': 1, 'D': 1},
#     'C': {'A': 1, 'B': 1, 'D': 1},
#     'D': {'B': 1, 'C': 1}
# distance = {node: float('infinity') for node in graph}
# distance['A'] = 0

def dijkstra(graph, start):
    print("dijkstra")
    distance = {node: float('infinity') for node in graph}
    distance[start] = 0
    print('Distances initalized')
    priority_queue = [(0, start)]

    while priority_queue:
        current_dist, current_node = heapq.heappop(priority_queue)

        if current_dist > distance[current_node]:
            continue

        for neighbor, weight in graph.edges(current_node):# if dict-of-dicts use graph[current_node].items():
            new_dist = distance[current_node] + weight
            if new_dist < distance[neighbor]:
                distance[neighbor] = new_dist
                heapq.heappush(priority_queue, (new_dist, neighbor))

    return distance

def shortest_path(graph, start, end):
    return nx.shortest_path(graph, start, end)
    # distances = dijkstra(graph, start)
    # path = [end]
    # while path[-1] != start:
    #     neighbors = graph.edges(path[-1]) #[path[-1]]
    #     previous_node = min(neighbors, ) # key=lambda node: distances[node])
    #     path.append(previous_node)
    # return path[::-1]

graph = generate_graph("mazesolver/mazesolver/maze_gen/large_example.txt")
start_node = (0,4) # no strings allowed
end_node = (11,5)
path = shortest_path(graph,start_node,end_node)

# print(shortest_distance)
# print("trying path")
# path = shortest_path(graph, start_node, end_node)

print(f"Waypoints: {path}")
# Put path
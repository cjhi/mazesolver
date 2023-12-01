# Example using an adjacency list for the graph representation
graph = {
    'A': {'B': 1, 'C': 1},
    'B': {'A': 1, 'C': 1, 'D': 1},
    'C': {'A': 1, 'B': 1, 'D': 1},
    'D': {'B': 1, 'C': 1}
}

distance = {node: float('infinity') for node in graph}
distance['A'] = 0


import heapq
priority_queue = [(0, 'A')]

def dijkstra(graph, start):
    distance = {node: float('infinity') for node in graph}
    distance[start] = 0

    priority_queue = [(0, start)]

    while priority_queue:
        current_dist, current_node = heapq.heappop(priority_queue)

        if current_dist > distance[current_node]:
            continue

        for neighbor, weight in graph[current_node].items():
            new_dist = distance[current_node] + weight
            if new_dist < distance[neighbor]:
                distance[neighbor] = new_dist
                heapq.heappush(priority_queue, (new_dist, neighbor))

    return distance

def shortest_path(graph, start, end):
    distances = dijkstra(graph, start)
    path = [end]

    while path[-1] != start:
        neighbors = graph[path[-1]]
        previous_node = min(neighbors, key=lambda node: distances[node])
        path.append(previous_node)

    return path[::-1]

start_node = 'A'
end_node = 'D'
shortest_distance = dijkstra(graph, start_node)[end_node]
path = shortest_path(graph, start_node, end_node)

print(f"Path: {path}")
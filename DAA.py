import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from itertools import permutations

# Define the warehouse layout as a graph
class WarehousePicking:
    def __init__(self, picking_points, distances):
        self.picking_points = picking_points
        self.distances = distances
        self.graph = nx.Graph()

        # Create the graph with picking points and distances
        for i, point in enumerate(picking_points):
            for j, dist in enumerate(distances[i]):
                if i != j:
                    self.graph.add_edge(point, picking_points[j], weight=dist)

    # Nearest Neighbor Algorithm for TSP
    def nearest_neighbor(self, start_point):
        unvisited = set(self.picking_points)
        unvisited.remove(start_point)
        tour = [start_point]
        current_point = start_point

        while unvisited:
            next_point = min(unvisited, key=lambda point: self.graph[current_point][point]['weight'])
            tour.append(next_point)
            unvisited.remove(next_point)
            current_point = next_point

        tour.append(start_point)  # Return to the starting point
        return tour

    # Calculate the total distance of a given tour
    def total_distance(self, tour):
        distance = 0
        for i in range(len(tour) - 1):
            distance += self.graph[tour[i]][tour[i + 1]]['weight']
        return distance

    # Visualize the tour
    def visualize_tour(self, tour):
        pos = nx.spring_layout(self.graph)
        plt.figure(figsize=(10, 6))

        nx.draw(self.graph, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=10)
        nx.draw_networkx_edges(self.graph, pos, edgelist=list(zip(tour, tour[1:])), edge_color='r', width=2)

        plt.title(f"Warehouse Picking Route: Total Distance = {self.total_distance(tour):.2f}")
        plt.show()

# Define picking points (nodes) in the warehouse
picking_points = ['A', 'B', 'C', 'D', 'E', 'F']

# Define distances between picking points (a symmetric matrix)
distances = [
    [0, 10, 15, 20, 10, 25],
    [10, 0, 35, 25, 17, 30],
    [15, 35, 0, 30, 15, 28],
    [20, 25, 30, 0, 18, 12],
    [10, 17, 15, 18, 0, 20],
    [25, 30, 28, 12, 20, 0]
]

# Initialize the WarehousePicking object
warehouse = WarehousePicking(picking_points, distances)

# Starting point for the picking route
start_point = 'A'

# Calculate the tour using the Nearest Neighbor heuristic
optimal_tour = warehouse.nearest_neighbor(start_point)
total_dist = warehouse.total_distance(optimal_tour)

print(f"Optimized Picking Route: {' -> '.join(optimal_tour)}")
print(f"Total Distance: {total_dist:.2f}")

# Visualize the optimized picking route
warehouse.visualize_tour(optimal_tour)

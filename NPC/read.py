import re
import sys
import networkx as nx
import matplotlib.pyplot as plt
from dataclasses import dataclass

# Create an empty graph
G = nx.Graph()

@dataclass
class Node:
    letter: str
    id: int

@dataclass
class Edge:
    a: int
    b: int


def foo(path):
	# Open the file
	with open(path, 'r') as file:
		content = file.read()

	# Extract node labels using regular expressions
	node_labels = re.findall(r'(\d+)\s*\[label=(\w+)\];', content)

	# Extract edges using regular expressions
	edges = re.findall(r'(\d+)\s*--\s*(\d+);', content)

	# Create a dictionary to store nodes
	nodes = {}

	# Create Node objects and store them in the dictionary
	for node_id, label in node_labels:
		node = Node(label, int(node_id))
		nodes[node_id] = label

	# Create a list to store edges
	graph_edges = []

	# Create Edge objects and append them to the list
	for node_a_id, node_b_id in edges:
		# node_a = nodes[int(node_a_id)]
		# node_b = nodes[int(node_b_id)]
		edge = Edge(node_a_id, node_b_id)
		graph_edges.append(edge)

	# Print the nodes
	print("Nodes:")
	for node_id in nodes:
		id : int = node_id
		lb : str = nodes[node_id]
		G.add_node(id, label=lb)
		print(f"ID: {id}, Letter: {lb}")

	# Print the edges
	print("Edges:")
	for edge in graph_edges:
		G.add_edge(edge.a, edge.b)
		print(f"A: {edge.a}, B: {edge.b}")


# Draw the graph
def draw_graph(graph):
	pos = nx.spring_layout(graph)  # Position the nodes using a spring layout algorithm
	labels = nx.get_node_attributes(graph, 'label')  # Get the node labels
	# print(nx.adjacency_matrix(G))
	nx.draw_networkx(graph, pos, labels=labels)
	plt.show()


# Depth-First Search (DFS)
def dfs(graph, start_node):
	visited = set()  # Set to keep track of visited nodes
	stack = [start_node]  # Stack for DFS traversal

	while stack:
		node = stack.pop()
		if node not in visited:
			print(node)
			visited.add(node)
			neighbors = graph.neighbors(node)  # Get neighbors of the current node
			stack.extend(neighbors)


# # Perform DFS traversal
# visited = set()  # Set to keep track of visited nodes

# def dfs(graph, node):
#     visited.add(node)
#     print(node)

#     neighbors = graph.neighbors(node)  # Get neighbors of the current node
#     for neighbor in neighbors:
#         if neighbor not in visited:
#             dfs(graph, neighbor)

# # Call the DFS function starting from node 1
# dfs(G, 1)

if __name__ == '__main__':
  foo(path=sys.argv[1].encode('utf-8'))
  dfs(G, 1)
  draw_graph(G)

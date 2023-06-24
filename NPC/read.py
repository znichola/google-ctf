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
		# node = Node(label, int(node_id))
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
	pos = nx.spring_layout(G)  # Position the nodes using a spring layout algorithm
	labels = nx.get_node_attributes(G, 'label')  # Get the node labels
	nx.draw_networkx(G, pos, labels=labels)
	plt.show()


if __name__ == '__main__':
  foo(path=sys.argv[1].encode('utf-8'))

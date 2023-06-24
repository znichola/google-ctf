import re
import sys
import networkx as nx
import matplotlib.pyplot as plt

# Create an empty graph
G = nx.Graph()

def foo(path):
	# Open the file
	with open(path, 'r') as file:
		content = file.read()

	# Extract node labels using regular expressions
	node_labels = re.findall(r'\[label=(\w+)\];', content)

	# Extract edges using regular expressions
	edges = re.findall(r'(\d+)\s*--\s*(\d+);', content)

	# Print the node labels
	print("Node Labels:")
	for node in node_labels:
		print(node)

	# Print the edges
	print("Edges:")
	for edge in edges:
		print(edge)


if __name__ == '__main__':
  foo(path=sys.argv[1].encode('utf-8'))

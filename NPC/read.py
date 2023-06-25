import re
import sys
import networkx as nx
import matplotlib.pyplot as plt
from dataclasses import dataclass

# gen list of words
def get_word_list():
	with open('given/USACONST.TXT', encoding='ISO8859') as f:
		text = f.read()
	return set(re.sub('[^a-z]', ' ', text.lower()).split())

# Create an empty graph
G = nx.Graph()

hasher = get_word_list()

def foo(path):
	# Open the file
	with open(path, 'r') as file:
		content = file.read()

	# Extract node labels using regular expressions
	node_labels = re.findall(r'(\d+)\s*\[label=(\w+)\];', content)

	# Extract edges using regular expressions
	edges = re.findall(r'(\d+)\s*--\s*(\d+);', content)

	# Create Node objects and store them in the dictionary
	for node_id, label in node_labels:
		G.add_node(int(node_id), label=label)

	# Create Edge objects and append them to the list
	for node_a_id, node_b_id in edges:
		G.add_edge(int(node_a_id), int(node_b_id))


# Print the nodes
def print_graph(g):
	print("Node:")
	for node in G.nodes:
		label = G.nodes[node]['label']  # Get the label of the node
		print(f"ID: {node}, Label: {label}")

	# Print the edges
	print("Edges:")
	for edge in g.edges:
		print(edge)


# Draw the graph
def draw_graph(g):
	pos = nx.spring_layout(g)  # Position the nodes using a spring layout algorithm
	labels = nx.get_node_attributes(g, 'label')  # Get the node labels
	# print(nx.adjacency_matrix(G))
	nx.draw_networkx(g, pos, labels=labels)
	# plt.show()
	plt.savefig("mygraph.png")




def dfs(node): # a list of node paths starting form the node

	# Perform DFS traversal
	visited = set()  # Set to keep track of visited nodes

	visited.add(node)

	neighbors = G.neighbors(node)  # Get neighbors of the current node
	for neighbor in neighbors:
		if neighbor not in visited:
			print("visited: ", neighbor)
			dfs(neighbor)


# def generate_and_test(vertices, subset):
# 	print("testing:", vertices)
# 	if not vertices:
# 		# Check if the subset induces a connected subgraph
# 		if nx.is_connected(G.subgraph(subset)):
# 			yield subset
# 	else:
# 		v = vertices[0]  # Choose a vertex v from the remaining vertices
# 		generate_and_test(vertices[1:], subset)
# 		generate_and_test(vertices[1:], subset + [v])


def visit(neighbors : set, to_visit : set, visited : list):
	# print(to_visit)
	# print(neibours)
	for n in neighbors:
		if n in to_visit:
			to_visit.remove(n)
			visited.append(n)
			if (len(visited) == len(G.nodes)):
				word = ''.join(str(G.nodes[i]['label']) for i in visited)
				if word in hasher:
					print(word)
				return
			# print(G.nodes[n]['label'], end='')
			visit(set(G.neighbors(n)), set(to_visit), list(visited))
			visited.pop()
			to_visit.add(n)
			# if len(to_visit) == 0:
				# print("")


if __name__ == '__main__':
	foo(path=sys.argv[1].encode('utf-8'))
	print_graph(G)

	all_nodes = list(G.nodes)

	# dfs(all_nodes[0])
	# subsets = generate_and_test(all_nodes, [])
	# print("Connected Subsets:")
	# for subset in subsets:
	# 	print(subset)

	# itterator for all the nodes
	for n in G:
		print(G.nodes[n]['label'], ": ", end='')

		# for each node we find it's neighbours
		for nei in G.neighbors(n):
			print(G.nodes[nei]['label'], end='')
		print("")

	for n in G:
		neighbors = set(G.neighbors(n))
		to_visit = set(G.nodes)
		to_visit.remove(n)
		visited : list = [n]

		# print("visiting : ", G.nodes[n]['label'], end=' ')
		visit(neighbors, to_visit, visited)
		# print("")
	# draw_graph(G)

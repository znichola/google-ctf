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

possible_words : set = get_word_list()

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
	print("Node : connedtions")
	for n in G:
		print("  ", G.nodes[n]['label'], "  ", end='')

		# for each node we find it's neighbours
		# and with comprehension to oneliner it
		print(''.join(str(G.nodes[i]['label']) for i in G.neighbors(n)))

# Draw the graph
def draw_graph(g):
	pos = nx.spring_layout(g)  # Position the nodes using a spring layout algorithm
	labels = nx.get_node_attributes(g, 'label')  # Get the node labels
	nx.draw_networkx(g, pos, labels=labels)
	# plt.show() # dosn't work on wsl, use below
	plt.savefig("mygraph.png")

# check all paths through the nodes that lead to full words
def visit(neighbors : set, to_visit : set, visited : list):
	for n in neighbors:
		if n in to_visit:
			to_visit.remove(n)
			visited.append(n)
			if (len(visited) == len(G.nodes)):
				word = ''.join(str(G.nodes[i]['label']) for i in visited)
				if word in possible_words:
					print(word)
				return
			visit(set(G.neighbors(n)), set(to_visit), list(visited))
			visited.pop()
			to_visit.add(n)

def find_word():
	print("single word password = ", end="")
	for n in G:
		neighbors = set(G.neighbors(n))
		to_visit = set(G.nodes)
		to_visit.remove(n)
		visited : list = [n]
		visit(neighbors, to_visit, visited)

if __name__ == '__main__':
	foo(path=sys.argv[1].encode('utf-8'))
	print_graph(G)
	find_word()


	# draw_graph(G)

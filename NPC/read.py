import re
import sys
import networkx as nx
import matplotlib.pyplot as plt
import pygtrie as trie
import math

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

# multiword password!

num_noded = len(G.nodes)

already_seen : set = {}

# word_trie = trie.StringTrie()
# word_trie["testthis"] = None
# word_trie["test_this"] = None
# word_trie["wizz"] = None
# word_trie["bag"] = None
# word_trie["bagbag_you_cut_me_down"] = None
# sdf = "testthis"
# print(word_trie.has_node(sdf) == trie.Trie.HAS_VALUE)
# print(word_trie.has_node(sdf) == trie.Trie.HAS_SUBTRIE)
# exit()

ordered_words = list(possible_words)
ordered_words.sort(reverse=False)
# print(ordered_words)

def bin_search(word : str):
	A = ordered_words
	n = len(A)
	L = 0
	R = n - 1
	while L <= R:
		m = int(math.floor((L + R) / 2))
		if A[m] < word:
			L = m + 1
		elif A[m] > word:
			R = m - 1
		else:
			return m
	return m

# wrd = "leg"
# n = bin_search(wrd)
#
# print(ordered_words[n].find(wrd))
# print(ordered_words[n-1], ordered_words[n], ordered_words[n+1])
# print(n)

# exit()

# check all paths through the nodes that lead to full words
def visit2(neighbors : set, to_visit : set, visited : list, so_far : list):
	for n in neighbors:
		if n in to_visit:
			to_visit.remove(n)
			visited.append(str(G.nodes[n]['label']))

			word = ''.join(visited)
			idx = bin_search(word)
			closet_word = ordered_words[idx]
			closet_word2 = ordered_words[idx+1]

			# only search short ifthere is a possible match
			if (not (closet_word.find(word) == -1
					and closet_word2.find(word) == -1)):
				if word == closet_word:
					print("    found:", word)

				# break if we've exhaused all nodes
				if (len(visited) == num_noded):
					return

				# recursivly call the function
				visit2(set(G.neighbors(n)), set(to_visit), list(visited), str(so_far))
			visited.pop()
			to_visit.add(n)

def find_multi_word():
	print("multi word password = ", end="")
	for n in G:
		neighbors = set(G.neighbors(n))
		to_visit = set(G.nodes)
		to_visit.remove(n)
		visited : list = [str(G.nodes[n]['label'])]
		print("starting with :", visited[0])
		visit2(neighbors, to_visit, visited, '')


if __name__ == '__main__':
	foo(path=sys.argv[1].encode('utf-8'))
	print_graph(G)
	# find_word()
	find_multi_word()

	# draw_graph(G)

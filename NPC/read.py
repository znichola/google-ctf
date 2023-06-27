import re
import sys
import networkx as nx
import matplotlib.pyplot as plt
import math
import copy
import pyrage

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

wrd = ["apple", "banna"]
w = ''.join(wrd)
f = "applebannaorange"

print(f.find(w))
print(f[len(w):])
# exit()

words_found : set = set()
words_found_nodes : list = list()

# check all paths through the nodes that lead to full words
def visit2(neighbors : set, to_visit : set, visited : list, vn : list, so_far : list):
	for n in neighbors:
		if n in to_visit:
			to_visit.remove(n)
			visited.append(str(G.nodes[n]['label']))
			vn.append(n)

			word = ''.join(visited)
			idx = bin_search(word)
			closet_word = ordered_words[idx]

			if idx == len(ordered_words) - 1:
				closet_word2 = closet_word
			else:
				closet_word2 = ordered_words[idx+1]

			# only search if there is a possible match
			if (not (closet_word.find(word) == -1
					and closet_word2.find(word) == -1)):
				if word == closet_word:
					# print("    found:", word)
					words_found.add(word)
					words_found_nodes.append(copy.deepcopy(vn))

				# break if we've exhaused all nodes
				if (len(visited) == num_noded):
					return

				# recursivly call the function
				visit2(set(G.neighbors(n)), set(to_visit), list(visited), list(vn), list(so_far))

			# undo last addition for backtracking
			visited.pop()
			vn.pop()
			to_visit.add(n)

def find_multi_word():
	# print("multi word password = ", end="")
	for n in G:
		neighbors = set(G.neighbors(n))
		to_visit = set(G.nodes)
		to_visit.remove(n)
		visited : list = [str(G.nodes[n]['label'])]
		# print("starting with :", visited[0])
		visit2(neighbors, to_visit, visited, [n], [])

def get_word(word):
	return ''.join([ G.nodes[w]['label'] for w in word ])

def make_set(words : list):
	s : set = set()
	s.add(123)
	for w in words:
		# print(w)
		# print(s)
		s = s & w
	return s

def rec_add(password : set, words_to_check : set, letters_left : set):
	# print("here", get_word(password))
	if len(letters_left) == 0:
		print("used all letters and nodes")
		return
	if password == letters_left:
		print("found", get_word(password))
		return
	for word in words_to_check:
		new_pass = password | word
		# print(get_word(new_pass), get_word(word), get_word(password ^ word))
		if new_pass == (password ^ word):
			rec_add(new_pass, words_to_check - word, letters_left)

possible_paths : list = list()

def find_matches(w, words : dict, all_nodes : set):
	# if all_nodes.issubset(set(w)):
	# 	print("\033[1;32m~~ wrd match:\033[0;0m ~~ ", words[w])
	# 	return (w)

	for i in words:
		# we know the two words are compatible
		if set(w).isdisjoint(i):
			# get last node in word
			last_letter = w[-1]
			first_letter = i[0]
			flag = 0
			# find if i follows from w
			if first_letter in set(nx.neighbors(G, last_letter)):
				# print("~~ sequence :", words[w], words[i])
				flag += 1

			# find if it's using all the nodes
			if all_nodes.issubset(set(w) | set(i)):
				# print("~~ is subset:", words[w], words[i])
				flag += 2
			if flag == 3:
				print("\033[1;32m~~     match:\033[0;0m", words[w] + words[i])
				possible_paths.append(words[w] + words[i])
				# return (w, i)

			# recursivly check
			if flag == 1:
				words2 = copy.deepcopy(words)
				words2.pop(w)
				words2.pop(i)
				w2 = tuple(list(w) + list(i))
				words2[w2] = str(words[w] + words[i])
				# print("~~     rec  :", words[w], words[i])
				ret = find_matches(w2, words2, all_nodes)
				if ret is not None:
					return ret
				# print("~~ leave rec:", words[w], words[i], "ret", ret)
	# only print them is they contain the full set of nodes


if __name__ == '__main__':
	foo(path=sys.argv[1].encode('utf-8'))
	print_graph(G)
	# find_word()
	find_multi_word()

	draw_graph(G)
	# exit()

	# print(words_found)
	# [G.nodes[l]['label'] for l in w]
	print([ ''.join([G.nodes[l]['label'] for l in w]) for w in words_found_nodes])
	# print(words_found_nodes)

	# use set math to figure out the right como of words I think

	all_nodes = set(G)
	words_set  = [tuple(s) for s in words_found_nodes]
	words_word = [get_word(w) for w in words_found_nodes]

	words = dict(zip(words_set, words_word))

	for w in words:
		# words2 = copy.deepcopy(words)
		# words2.pop(w)
		find_matches(w, words, all_nodes)

	print("attempting decryption .. ")
	for p in possible_paths:
		print("with password:", p, end="")
		with open(sys.argv[2], 'rb') as f:
			encrypted = f.read()
			try:
				decrypted = pyrage.passphrase.decrypt(encrypted, p)
				print(" yes!, flag is: ", decrypted)
			except:
				print(" .. nope")

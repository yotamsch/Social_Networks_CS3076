import collections
import networkx as nx
import matplotlib.pyplot as plt
import random

# Question 3a. 
# The function return True iff the graph G is balanced. 
# Assumption: Each edge has an attribute 'label' with a value '+' or '-', 
# as in the example at Recitation 3.
def check_balance(G):
    # The choice to use cycle_basis is influenced by one of the suggestions here:
    # https://stackoverflow.com/questions/1705824/finding-cycle-of-3-nodes-or-triangles-in-a-graph
	triangles = [c for c in nx.cycle_basis(G) if len(c)==3]
	non_balanced_triangles = [t for t in triangles if not is_balanced_triangle(G, t)]
	# If all triangles in G are balanced, the list 'non_balanced_triangles' is empty.
	return (len(non_balanced_triangles) == 0)
	
# Question 3b. The argument 'plus_probability' is the probability of
# an edge to be labeled with the '+' sign.
def getSignedErdosRenyiGraph(plus_probability):
	# n=30, p=0.5 are fixed, according to the instructions in 3b.
	n = 30
	p = 0.5
	G=nx.Graph()
	
	# Add all graph nodes.
	for i in range (0, n):
		G.add_node(i)
	
	# Pass over n(n-1)/2 potential edges. Reminder:
	# (n-1) + (n-2) + ... + 1 = n(n-1)/2
	for i in range (0,n-1):
		for j in range (i+1,n):
			coin = random.uniform(0, 1)
			if coin <= p:
				sign_coin = random.uniform(0, 1)
				if sign_coin <= plus_probability:
					G.add_edge(i, j, label='+')
				else:
					G.add_edge(i, j, label='-')

	return G

# Helper function of 3a. Returns true iff the given triangle t is
# balanced in the graph G.
# Implementation note:
# According to page 31 in lecture 3, a triangle is balanced iff its
# amount of 'plus' labeled edges, is different than 2.
def is_balanced_triangle(G, t):
	# It is important to keep the smaller indexed node in the Left position,
	# as this is how the output of 'get_edge_attributes' is arranged.
	u = (t[0], t[1]) if t[0] < t[1] else (t[1], t[0])
	v = (t[1], t[2]) if t[1] < t[2] else (t[2], t[1])
	w = (t[0], t[2]) if t[0] < t[2] else (t[2], t[0])

	# Count the number of edges with a '+' label.
	plus_counter = 0
	
	# Get a dictionary, containing the label attribute of each
	# edge in the graph.
	edge_labels = nx.get_edge_attributes(G, 'label')
	
	# Increase counter as necessary:
	if edge_labels[u] == '+':
		plus_counter += 1
	if edge_labels[v] == '+':
		plus_counter += 1
	if edge_labels[w] == '+':
		plus_counter += 1

	return (plus_counter != 2)

# Helper of 3c.
def analyze_random_ER_graph(plus_probability):
	print("Generating an ER graph with n=30, p=0.5, label='+' with a probability of  " + str(plus_probability) + ":")
	G = getSignedErdosRenyiGraph(plus_probability)
	print("The generated graph is " + ("balanced." if check_balance(G) else "not balanced."))
	show_graph(G)

# Helper of 3c.
def show_graph(G):
	print("Yotam please implement if you have time.")

# Main function	
def main():
	analyze_random_ER_graph(0.9)
	analyze_random_ER_graph(0.5)

if __name__ == "__main__":
    main()
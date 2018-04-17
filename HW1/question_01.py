import collections
import networkx as nx
import matplotlib.pyplot as plt
import random
import time

# Nodes will be numbered from 0 to n-1.

# Question 1a.
def getErdosRenyiGraph(n, p):
	G=nx.Graph()
	for i in range(0,n):
		G.add_node(i)
	# Pass over n(n-1)/2 potential edges. Reminder:
	# (n-1) + (n-2) + ... + 1 = n(n-1)/2
	for i in range (0,n-1):
		for j in range (i+1,n):
			coin = random.uniform(0, 1)
			if coin <= p:
				G.add_edge(i, j)
	return G

# Question 1b.
def getSmallWorldGraph(n, K, p):
	if K>n-1 or p<0 or p>1:
		return 'Invalid input values.'

	G = getRegularRingLattice(n, K)
	for i in range (0,n-1):
		for j in range (i+1,n):
			if G.has_edge(i,j): # Delete and re-wire in probability p.
				coin = random.uniform(0, 1)
				if coin <= p:
					G.remove_edge(i,j)
					non_neighbors_list = getNonNeighbords(G,i,n)
					candidate_node_index = random.randint(0, len(non_neighbors_list) -1)
					candidate_node = non_neighbors_list[candidate_node_index]
					G.add_edge(i, candidate_node)

	return G

# Question 1c.
# Returns the clustering coefficient of a given Graph.
def getGraphCC(G):
	sumCC = 0
	nodes = list(G.nodes())

	for node in nodes:
		sumCC += getNodeCC(G,node)

	return sumCC / len(nodes)

# All functions below are helpers.

# Helper function of 1b.
# Returns a graph with n nodes, in which each node has an edge with its
# int(K/2) nodes from left and right.
def getRegularRingLattice(n, K):
	G = nx.Graph()
	for i in range (0,n):
		candidates = getKNeighborhood(i, K, n)
		for j in candidates:
			if not G.has_edge(i,j):
				G.add_edge(i, j)

	return G

# Helper function of 1b.
# Returns a list of nodes belonging to the "K close neighborhood",
# according to the definition of a regular ring lattice. O(K) complexity.
def getKNeighborhood(i, K, n):
	max_distance = int(K/2)
	k_neighborhood = []
	
	for j in range (1, max_distance+1):
		upper_candidate = (i+j) % n
		lower_candidate = (i-j) % n
		if lower_candidate not in k_neighborhood:
			k_neighborhood.append(lower_candidate)
		if upper_candidate not in k_neighborhood:
			k_neighborhood.append(upper_candidate)

	return k_neighborhood

# Helper function of 1b. Get non-neighbors list of node i, and graph G,
# which contains n nodes (numbered from 0 to n-1).
def getNonNeighbords(G,i,n):
	i_neighbors = list(G.neighbors(i))
	non_i_neighbors = [j for j in range (0,n) if (j not in i_neighbors)]
	return non_i_neighbors

# Helper function of 1c.
# Returns the clustering coefficient of a given node i in graph G.
def getNodeCC(G, i):
	neighbors_list = list(G.neighbors(i))
	degree = len(neighbors_list)
	if degree<2:
		return 0
	connected_neighbors = 0
	
	for i in range(0,degree-1):
		for j in range(i+1,degree):
			connected_neighbors += (1 if (G.has_edge(neighbors_list[i], neighbors_list[j])) else 0)

	return (2 * connected_neighbors / (degree * (degree-1)))

# Helper function of 1d.
# Show a degree histogram of a given graph. As it's being used for Analysis and not a
# standalone task, the implementation is heavily based on:
# https://networkx.github.io/documentation/stable/auto_examples/drawing/plot_degree_histogram.html
def showDegreeHist(G, graphType):
	degree_sequence = sorted([degree for node, degree in G.degree()], reverse=True)  # degree sequence
	degreeCount = collections.Counter(degree_sequence)
	deg, cnt = zip(*degreeCount.items())
	_, ax = plt.subplots()
	plt.bar(deg, cnt, width=0.80, color='b')
	plt.title("Degree Histogram of " + graphType)
	plt.ylabel("Count")
	plt.xlabel("Degree")
	ax.set_xticks([d for d in deg])
	ax.set_xticklabels(deg, rotation=-45)
	# draw graph in inset
	plt.axes([0.4, 0.4, 0.5, 0.5])
	_ = sorted(nx.connected_component_subgraphs(G), key=len, reverse=True)[0]
	# Show the histogram
	plt.axis('off')
	plt.show()

	# Show the network (graph)
	plt.clf() # clear the current figure for clean graph printing
	pos = nx.spring_layout(G)
	nx.draw_networkx_nodes(G, pos, node_size=20)
	nx.draw_networkx_edges(G, pos, alpha=0.4)
	plt.show()

# Helper function of 1d.
# Print the desired measures of section 1d.
def performAnalysis(G, graphType):
	if type(G) is str:
		print(G) # Invalid arguments.
		return
	
	diameter = -1 if not nx.is_connected(G) else nx.diameter(G)
	if diameter == -1:
		diameter = "Infinity is graph is not connected"
	else:
		diameter = str(diameter)
	
	print("Clustering coeff is " + str(getGraphCC(G)) + ", and its diameter is " + diameter)
	showDegreeHist(G, graphType)

def main():
	t1 = time.time()
	G_ER = getErdosRenyiGraph(1000, 0.2)
	performAnalysis(G_ER , "an Erdos Renyi Graph")

	G_SW = getSmallWorldGraph(1000, 8, 0.1)
	performAnalysis(G_SW, "a Small World Graph")
	print("Runtime: %.3f seconds" % (time.time() - t1))

if __name__ == "__main__":
    main()

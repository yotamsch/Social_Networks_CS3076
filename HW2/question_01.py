import collections
from collections import OrderedDict
import networkx as nx
import matplotlib.pyplot as plt

# Question 1a.
def printCommunities(G, k):
	# Get connected components.
	if len(G)<k:
		print("Given graph has less than " + str(k) + " nodes, so cannot have " + str(k) + " communities")
		return
	components = list(nx.connected_component_subgraphs(G))
	while True:
		#components_counter = 0
		if len(components)>=k:
			break
		edges_to_remove = getHighestScoredEBEdges(G)
		if len(edges_to_remove)==0:
			break
		for edge in edges_to_remove:
			G.remove_edge(*edge)
		components = list(nx.connected_component_subgraphs(G))
	
	# Print the connected components.
	counter=0
	for component in components:
		counter=counter+1
		print("Community number " + str(counter) + " contains the following " + str(len(component)) + " nodes:")
		print(component.nodes())

# Question 1a helper. Add to the value of each entry in edges_EB_dict, the
# appropriate edge weight as defined in lecture 5, when source_node is the
# source of the BFS try built from graph G. 
def updateScoresAccordingToBfsFromNode(source_node, edges_EB_dict, G):
	# Create a dictionary in which, every node is mapped to its Predecessor.
	pred_dict = dict(nx.bfs_predecessors(G, source_node)) 
	added_edges_dict = {} # maps edge to its EB score
	while True:
		# find minimum weight edges (those which their destination node has an output degree of 0,
		# meaning: it is not a Predecessor of Any other node)
		min_weight_edges = [(pred_dict[u], u) for u in pred_dict.keys() if u not in pred_dict.values()]
		
		# Stop if no such edges exist.
		if len(min_weight_edges)==0:
			break
		# Set the EB score of each such (current) min weight edge, while Bubbling up
		# scores of its (direct) children edges. 
		for edge in min_weight_edges:
			added_edges_dict[edge]=1
			bubble_up_edges = [x for x in added_edges_dict.keys() if edge[1]==x[0]]
			for bubble_edge in bubble_up_edges:
				added_edges_dict[edge]= added_edges_dict[edge] + added_edges_dict[bubble_edge]
		# Remove current bottom nodes from the predecessors dictionary.
		for edge in min_weight_edges:
			pred_dict.pop(edge[1])
		
		if len(pred_dict)==0:
			break
			
	for edge in added_edges_dict.keys():
		if edge in edges_EB_dict.keys():
			edges_EB_dict[edge] = edges_EB_dict[edge] + added_edges_dict[edge]
		else:
			reverse_edge = (edge[1],edge[0])
			if reverse_edge in edges_EB_dict.keys():
				edges_EB_dict[reverse_edge] = edges_EB_dict[reverse_edge] + added_edges_dict[edge]			
			

# Question 1a helper. Returns a list, containing the edge/s which received the maximum
# EB score.
def getHighestScoredEBEdges(G):
	# Prepare a dictionary which maps each edge to its EB score (actually,
	# twice its EB score, as the 2 factor doesn't affect choosing the max
	# scored edge/s).
	edges_EB_dict = {edge:0 for edge in list(G.edges())}
	nodes_list = list(G.nodes())
	for source_node in nodes_list:
		updateScoresAccordingToBfsFromNode(source_node, edges_EB_dict, G)
	
	# Theoretically, we should devide all EB scores by 2, however
	# it won't affect the final result.
	# for edge in edges_EB_dict.keys():
	#	edges_EB_dict[edge] = (edges_EB_dict[edge]/2)
	
	# Sort EB scores in descending order.
	sorted_edges_by_EB = OrderedDict(sorted(edges_EB_dict.items(), key=lambda t: t[1], reverse = True))
	max_EB = -1              # uninitialized max EB score.
	max_scored_EB_edges = [] # empty list.
	
	# Add all max scored edges (those which receive the highest EB score) to the
	# result list.
	for edge, eb in sorted_edges_by_EB.items():
		if max_EB == -1:
			max_EB = eb
			max_scored_EB_edges.append(edge)
		elif eb==max_EB:
			max_scored_EB_edges.append(edge)
		else:
			break
	
	return max_scored_EB_edges

# Question 1b helper.
def	buildGraphFromFile(file_name):
	H=nx.Graph()
	input_file = open(file_name, "r")
	for line in input_file:
		u,v = line.split(" ")
		u = int(u)
		v = int(v)
		if (u<0 or v<0):
			print("unsuccessful parsing of edges nodes: (" + str(u) + ", " + str(v) + ")")
			continue
		H.add_edge(u,v)
	print("Size of graph extracted from input file is " + str(len(H)))
	return H
	
# Question 1b helper.
def	getSubgraphOfBiggestConnectedComponent(H):
	G = max(nx.connected_component_subgraphs(H), key=len)
	print("Biggest connected component's size is " + str(len(G)))
	return G
	
# Main.
H = buildGraphFromFile("communities.txt")
G = getSubgraphOfBiggestConnectedComponent(H)
printCommunities(G, 3)
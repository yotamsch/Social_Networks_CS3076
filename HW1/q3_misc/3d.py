import collections
import networkx as nx
import matplotlib.pyplot as plt
import random

# Question 3d. The values of f(x) as defined in the PDF, were hard coded
# here. As an exception, the nodes will be numbered from 1 (as in the PDF).
def CreateMallsSignedGraph():
	G=nx.Graph()
	# Add all graph nodes (each represent a mall).
	# One mall has f==700.
	G.add_node(1, f=700)
	# Three malls have f==750.
	G.add_node(2, f=750)
	G.add_node(3, f=750)
	G.add_node(4, f=750)
	# Six malls have f==800.
	G.add_node(5, f=800)
	G.add_node(6, f=800)
	G.add_node(7, f=800)
	G.add_node(8, f=800)
	G.add_node(9, f=800)
	G.add_node(10, f=800)
	# One mall has f==850.
	G.add_node(11, f=850)
	# Two malls have f==900.
	G.add_node(12, f=900)
	G.add_node(13, f=900)	
	# Two malls have f==950.
	G.add_node(14, f=950)
	G.add_node(15, f=950)
	
	# Get the attribute f of all the nodes.
	f=nx.get_node_attributes(G,'f')
	
	# Create the edges:
	for i in range (1,15):
		for j in range (i+1,16):
			if (f[i] == f[j]):
				G.add_edge(i, j, label='+')
			else:
				G.add_edge(i, j, label='-')
	
	# get the edges of the graph to later draw _r means regular, _R means balded
	eplus_r = [(u,v) for (u,v,d) in G.edges(data=True) if d['label'] =='+']
	eminus_r = [(u,v) for (u,v,d) in G.edges(data=True) if d['label'] == '-']
	
	# Retrieve the positions from graph nodes and save to a dictionary
	pos = nx.spring_layout(G)

	# Draw nodes
	nx.draw_networkx_nodes(G,pos,node_color='#cccccc',node_size=300)
	
	# Draw edges
	nx.draw_networkx_edges(G,pos,edgelist=eplus_r, width=2, edge_color='g', alpha=1)
	nx.draw_networkx_edges(G,pos,edgelist=eminus_r, width=2, edge_color='r', alpha=1, style='dashed')
	
	# Draw node labels
	nx.draw_networkx_labels(G,pos,font_color='#333333',font_family='sans-serif')
	
	plt.axis('off')
	plt.show()


def main():
	CreateMallsSignedGraph()


if __name__ == "__main__":
    main()
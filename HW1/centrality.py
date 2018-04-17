import networkx as nx

"""
A simple BFS implementation. Returns two dictionaries:
    1. dictionary of the shape { node : distance }.
"""
def simpleBFS(G, node):
    # the idea is getting the distances of each node to the other nodes with bfs
    # I'm not sure what was expected and if i needed to implement bfs or not,
    # but I did.
    queue = [] # will have nodes for BFS usage
    distance = {} # distances
    queue.append(node)
    distance[node] = 0

    while len(queue) != 0:
        # pop item from the top of the quq
        n = queue[0]
        queue.remove(n)
        # go over all the child nodes
        for nxt_n in G.neighbors(n):
            # if visited before
            if nxt_n in distance:
                continue
            # push the child node to the queue
            queue.append(nxt_n)
            # add the distance based on the distance of the parent
            distance[nxt_n] = distance[n] + 1

    return distance

"""
This functions gets a graph and returns a dictionary of the shape { node : degree-centrality-value }.
"""
def degree(G, node=None):
    if not node:
        nodes = G.nodes()
    else:
        nodes = [node]
    
    result = {}
    num_of_nodes = len(G.nodes())

    for n in nodes:
        node_degree = len(list(G.neighbors(n)))
        result[n] = node_degree / (num_of_nodes - 1)
    return result

"""
This functions gets a graph and returns a dictionary of the shape { node : betweeness-centrality-value }.
"""
def betweenness(G, node=None):
    if not node:
        nodes = G.nodes()
    else:
        nodes = [node]

    num_of_nodes = len(G.nodes())
    result = dict(zip(nodes,[0 for t in range(num_of_nodes)]))

    for n in nodes:
        for nn in nodes:
            if n < nn:
                paths = [p for p in nx.all_shortest_paths(G,source=n,target=nn)]
                for p in paths:
                    for n_i in p[1:-1]:
                        if n_i in result:
                            result[n_i] += 1/len(paths)

    for res in result:
        result[res] *= 2
        result[res] /= (num_of_nodes - 1)* (num_of_nodes - 2)
    
    return result

"""
This functions gets a graph and returns a dictionary of the shape { node : closeness-centrality-value }.
"""
def closeness(G, node=None):
    if not node:
        nodes = G.nodes()
    else:
        nodes = [node]
    
    result = {}
    num_of_nodes = len(G.nodes())

    for n in nodes:
        ds = simpleBFS(G,n)
        c_i = (num_of_nodes - 1) * pow(sum(ds.values()),-1)
        result[n] = c_i

    return result


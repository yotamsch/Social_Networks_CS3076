import networkx as nx

"""
A simple BFS implementation. Returns two dictionaries:
    1. dictionary of the shape { node : distance }.
    2. dictionary of the shape { node : {nodes-in-shortest-path}}
"""
def simpleBFS(G, node):
    # the idea is getting the distances of each node to the other nodes with bfs
    # I'm not sure what was expected and if i needed to implement bfs or not,
    # but I did.
    queue = [] # will have nodes for BFS usage
    distance = {} # distances
    s_paths = {} # shortest paths
    queue.append(node)
    distance[node] = 0
    ss_paths = []
    s_paths[node] = []

    while len(queue) != 0:
        # pop item from the top of the quq
        n = queue[0]
        queue.remove(n)
        # go over all the child nodes
        for nxt_n in G.neighbors(n):
            # if visited before
            if nxt_n in distance:
                # maybe part of shortest path
                if distance[nxt_n] == distance[n] + 1:
                    # fetch the parent path + the parent node
                    # add to path nodes pool
                    s_paths[nxt_n].extend(s_paths[n])
                    s_paths[nxt_n].append(n)
                continue
            # push the child node to the queue
            queue.append(nxt_n)
            # add the distance based on the distance of the parent
            distance[nxt_n] = distance[n] + 1
            # create shortest path node pool and update
            s_paths[nxt_n] = []
            s_paths[nxt_n].extend(s_paths[n])
            if n != node:
                # prevent (node -> node)
                s_paths[nxt_n].append(n)

    #print("\n%s:\n\t%s" % (node, s_paths))
    return distance, s_paths

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

    result = {}
    full_sp = {}

    for n in nodes:
        result[n] = 0
        _, sp = simpleBFS(G,n)
        for sp_k, sp_v in sp.items():
            if n < sp_k:
                full_sp[(n,sp_k)] = sp_v

    for _, sp_nodes_list in full_sp.items():
        for n in sp_nodes_list:
            result[n] += 1

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
        ds, _ = simpleBFS(G,n)
        c_i = (num_of_nodes - 1) * pow(sum(ds.values()),-1)
        result[n] = c_i

    return result


"""Set of functions to analyze connections within a graph"""

def copy_graph(graph):
    """
    Make a copy of a graph
    """
    new_graph = {}
    for node in graph:
        new_graph[node] = set(graph[node])
    return new_graph

def delete_node(ugraph, node):
    """
    Delete a node from an undirected graph
    """
    neighbors = ugraph[node]
    ugraph.pop(node)
    for neighbor in neighbors:
        ugraph[neighbor].remove(node)
    
def targeted_order(ugraph):
    """
    Compute a targeted attack order consisting
    of nodes of maximal degree
    
    Returns:
    A list of nodes
    """
    # copy the graph
    new_graph = copy_graph(ugraph)
    
    order = []    
    while len(new_graph) > 0:
        max_degree = -1
        for node in new_graph:
            if len(new_graph[node]) > max_degree:
                max_degree = len(new_graph[node])
                max_degree_node = node
        
        neighbors = new_graph[max_degree_node]
        new_graph.pop(max_degree_node)
        for neighbor in neighbors:
            new_graph[neighbor].remove(max_degree_node)

        order.append(max_degree_node)
    return order
    


import random
from collections import deque
def bfs_visited(ugraph,start_node):
    """generates a set of all nodes in ugraph connected to start_node"""
    node_queue = deque([start_node])
    visited = set([start_node])
    while len(node_queue)>0:
        current_node = node_queue.popleft()
        for neighbor in ugraph[current_node]:
            if neighbor not in visited:
                visited = visited.union([neighbor])
                node_queue.append(neighbor)

    return visited

def cc_visited(ugraph):
    """returns a set of connected nodes for each node in ugraph in a list"""
    remaining_nodes = set(ugraph.keys())
    connected_components = []
    while len(remaining_nodes) > 0:
        #node = remaining_nodes[0]
        current_set = bfs_visited(ugraph,random.sample(remaining_nodes,1)[0])
        #if current_set in connected_components:
        #    pass
        #else:
        connected_components.append(current_set)
        remaining_nodes= remaining_nodes - current_set
    return connected_components

def largest_cc_size(ugraph):
    """returns the length of the largest set of connected nodes"""
    all_sets = cc_visited(ugraph)
    if all_sets == []:
        largest = 0
    else:
        largest = max([len(dummy_x)for dummy_x in all_sets])
    return largest

def compute_resilience(ugraph,attack_order):
    """tracks the largest connected node size as nodes are removed"""
    clone = dict(ugraph)
    longest_list = [largest_cc_size(clone)]
    for attack in attack_order:
        delete_node(clone,attack)
##        del clone[attack]
##        for key in clone.keys():
##            if attack in clone[key]:
##                neighbors = clone[key]
##                new_neighbors = [x for x in neighbors if x != attack]
##                clone[key]=new_neighbors
        longest_list.append(largest_cc_size(clone))
        
    return longest_list

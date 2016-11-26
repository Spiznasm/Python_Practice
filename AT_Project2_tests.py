"""Set of functions to analyze connections within a graph"""
# general imports
import urllib2
import random
import time
import math
from timeit import default_timer as timer

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
    #start = timer()
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
    #end = timer()
    #print (end-start)
    return order

def fast_targeted_order(graph):
    
    ugraph = copy_graph(graph)
    #start = timer()
    degreesets = []
    for k in range(len(ugraph)):
        degreesets.append(set([]))
    for i in range(len(ugraph)):
        d = len(ugraph[i])
        degreesets[d].add(i)
    ordered_nodes = []
    
    for k in list(reversed(range(len(ugraph)))):
        while len(degreesets[k])>0:
            u = random.choice(list(degreesets[k]))
            degreesets[k].remove(u)
            for neighbor in ugraph[u]:
                
                d = len(ugraph[neighbor])
                if len(degreesets[d])>0:
                    degreesets[d].remove(neighbor)
                degreesets[d-1].add(neighbor)
            ordered_nodes.append(u)
            delete_node(ugraph,u)
    #end = timer()
    #print (end-start)
    return ordered_nodes
                



from collections import deque
def bfs_visited(ugraph,start_node):
    """generates a set of all nodes in ugraph connected to start_node"""
    node_queue = deque([start_node])
    visited = set([start_node])
    while len(node_queue)>0:
        current_node = node_queue.popleft()
        for neighbor in ugraph[current_node]:
            if neighbor not in visited:
                visited.add(neighbor)
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

"""
Provided code for Application portion of Module 2
"""



# CodeSkulptor import
#import simpleplot
#import codeskulptor
#codeskulptor.set_timeout(60)

# Desktop imports
import matplotlib.pyplot as plt


############################################
# Provided code



##########################################################
# Code for loading computer network graph

NETWORK_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_rf7.txt"


def load_graph(graph_url):
    """
    Function that loads a graph given the URL
    for a text representation of the graph
    
    Returns a dictionary that models a graph
    """
    graph_file = urllib2.urlopen(graph_url)
    graph_text = graph_file.read()
    graph_lines = graph_text.split('\n')
    graph_lines = graph_lines[ : -1]
    
    print "Loaded graph with", len(graph_lines), "nodes"
    
    answer_graph = {}
    for line in graph_lines:
        neighbors = line.split(' ')
        node = int(neighbors[0])
        answer_graph[node] = set([])
        for neighbor in neighbors[1 : -1]:
            answer_graph[node].add(int(neighbor))

    return answer_graph


def er_graph(num_nodes,prob):
    """Generates a random graph with num_nodes nodes and randomly placed edges
based on probablility prob"""
    if num_nodes < 1:
        return dict()
    else:
        new_dict = dict()
        for node in range(num_nodes):
            new_dict[node]=set([])
        for node in range(num_nodes):
            for edge in range(node):
                if random.random()<prob:
                    new_dict[node].add(edge)
                    new_dict[edge].add(node)
            
##            other_nodes = range(num_nodes)
##            other_nodes.pop(node)
##            new_dict[node]=set([])
##            for edge in other_nodes:
##                if random.random()<=prob:
##                    new_dict[node].add(edge)
             
        return new_dict

def random_order(ugraph):
    keys = ugraph.keys()
    random.shuffle(keys)
    return keys

class UPATrial:
    """
    Simple class to encapsulate optimizated trials for the UPA algorithm
    
    Maintains a list of node numbers with multiple instance of each number.
    The number of instances of each node number are
    in the same proportion as the desired probabilities
    
    Uses random.choice() to select a node number from this list for each trial.
    """

    def __init__(self, num_nodes):
        """
        Initialize a UPATrial object corresponding to a 
        complete graph with num_nodes nodes
        
        Note the initial list of node numbers has num_nodes copies of
        each node number
        """
        self._num_nodes = num_nodes
        self._node_numbers = [node for node in range(num_nodes) for dummy_idx in range(num_nodes)]


    def run_trial(self, num_nodes):
        """
        Conduct num_nodes trials using by applying random.choice()
        to the list of node numbers
        
        Updates the list of node numbers so that each node number
        appears in correct ratio
        
        Returns:
        Set of nodes
        """
        
        # compute the neighbors for the newly-created node
        new_node_neighbors = set()
        for _ in range(num_nodes):
            new_node_neighbors.add(random.choice(self._node_numbers))
        
        # update the list of node numbers so that each node number 
        # appears in the correct ratio
        self._node_numbers.append(self._num_nodes)
        for dummy_idx in range(len(new_node_neighbors)):
            self._node_numbers.append(self._num_nodes)
        self._node_numbers.extend(list(new_node_neighbors))
        
        #update the number of nodes
        self._num_nodes += 1
        return new_node_neighbors

##import collections    
##def UPA(n,m):
##    node_holder = UPATrial(m)
##    for dummy_idx in range(n-m):
##        node_holder.run_trial(m)
####    return node_holder
##    UPA_in_degrees = collections.Counter(node_holder._node_numbers)
##    return collections.Counter(UPA_in_degrees.values())
def make_complete_graph(num_nodes):
    """ returns a dictionary whose keys are nodes 0-num_nodes-1 and
    values are every other node"""
    if num_nodes < 1:
        return dict()
    else:
        new_dict = dict()
        for node in range(num_nodes):
            other_nodes = range(num_nodes)
            other_nodes.pop(node)
            new_dict[node]=set(other_nodes)
        return new_dict
    
def upa_graph(nodes,edges,start_size):
    start_graph = make_complete_graph(start_size)
    for new_node in range(nodes - start_size):
        neighbors = random.sample(start_graph.keys(),edges)
        next_node = len(start_graph.keys())
        for neighbor in neighbors:
            start_graph[neighbor].add(next_node)
        start_graph[next_node]=set(neighbors)
    return start_graph
    
network = load_graph(NETWORK_URL)

def edge_count(ugraph):
    total_edges = 0
    for node in ugraph:
        total_edges += len(ugraph[node])
    return total_edges/2


upa_version = upa_graph(1239,2,36)
er_version = er_graph(1239,.004)

#network_resilience = compute_resilience(network,random_order(network))
#upa_resilience = compute_resilience(upa_version,random_order(upa_version))
#er_resilience = compute_resilience(er_version,random_order(er_version))

import matplotlib.pyplot as plt

def legend_example():
    """
    Plot an example with two curves with legends
    """
    xvals = range(1240)
    yvals1 = network_resilience
    yvals2 = er_resilience
    yvals3 = upa_resilience
    
    plt.xlabel("Number of Nodes Removed")
    plt.ylabel("Longest Connected Set")
    plt.title("Resilience Comparison")
    plt.plot(xvals, yvals1, '-b', label='network')
    plt.plot(xvals, yvals2, '-r', label='er graph p=.004')
    plt.plot(xvals, yvals3, '-g', label='upa graph m=2')
    plt.legend(loc='upper right')
    plt.show()

#legend_example()

def time_graph(function):
    times = []
    for size in range(10,1000,10):
        graph = upa_graph(size,5,5)
        start = timer()
        function(graph)
        end = timer()
        times.append(end-start)
    return times

#targeted_runtime = time_graph(targeted_order)
#fast_runtime = time_graph(fast_targeted_order)

def attack_comparison():
    xvals = range(10,1000,10)
    yvals1 = targeted_runtime
    yvals2 = fast_runtime

    plt.xlabel("Number of Nodes")
    plt.ylabel("Runtime")
    plt.title("Runtime of targeted_order vs. fast_targeted_order on Desktop Python")
    plt.plot(xvals,yvals1,'-b', label='targeted_order')
    plt.plot(xvals,yvals2,'-r',label='fast_targeted_order')
    plt.legend(loc='upper left')
    plt.show()

#attack_comparison()

network_resilience = compute_resilience(network,targeted_order(network))
upa_resilience = compute_resilience(upa_version,targeted_order(upa_version))
er_resilience = compute_resilience(er_version,targeted_order(er_version))

def targeted_attack_graph():
    """
    Plot an example with two curves with legends
    """
    xvals = range(1240)
    yvals1 = network_resilience
    yvals2 = er_resilience
    yvals3 = upa_resilience
    
    plt.xlabel("Number of Nodes Removed")
    plt.ylabel("Longest Connected Set")
    plt.title("Resilience Comparison with Targeted Attack")
    plt.plot(xvals, yvals1, '-b', label='network')
    plt.plot(xvals, yvals2, '-r', label='er graph p=.004')
    plt.plot(xvals, yvals3, '-g', label='upa graph m=2')
    plt.legend(loc='upper right')
    plt.show()

targeted_attack_graph()

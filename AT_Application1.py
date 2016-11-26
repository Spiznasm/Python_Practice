"""Functions to compute the distribution of directed graphs"""
#Constants that will be used for testing
EX_GRAPH0 = {0:set([1,2]),1:set([]),2:set([])}
EX_GRAPH1 = {0:set([1,4,5]),1:set([2,6]),2:set([3]),3:set([0]),
             4:set([1]),5:set([2]),6:set([])}
EX_GRAPH2 = {0:set([1,4,5]),1:set([2,6]),2:set([3,7]),3:set([7]),
             4:set([1]),5:set([2]),6:set([]),7:set([3]),8:set([1,2]),
             9:set([0,4,5,6,7,3])}

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

def compute_in_degrees(digraph):
    """returns a dictionary whose keys are each node and values are that
    nodes in-degree"""
    if type(digraph)!= dict:
        return "Incorrect input"
    else:
        in_dict = dict()
        for node in digraph.keys():
            in_dict[node]=0
        for connected_nodes in digraph.values():
            for node in connected_nodes:
                in_dict[node]+=1
        return in_dict

def in_degree_distribution(digraph):
    """ returns a dictionary whose keys are an in-degree and values are
    the number of nodes with that degree"""
    if type(digraph)!= dict:
        return "Incorrect input"
    else:
        distribution = dict()
        for degree in compute_in_degrees(digraph).values():
            if degree in distribution:
                distribution[degree]+=1
            else:
                distribution[degree]=1
        return distribution

            
"""
Provided code for Application portion of Module 1

Imports physics citation graph 
"""

# general imports
import urllib2
import numpy as np
import matplotlib.pyplot as plt
import math


# Set timeout for CodeSkulptor if necessary
#import codeskulptor
#codeskulptor.set_timeout(20)


###################################
# Code for loading citation graph

CITATION_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_phys-cite.txt"

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

##citation_graph = load_graph(CITATION_URL)

##degree_dict = in_degree_distribution(citation_graph)
##normal_dist = {}
##for key in degree_dict.keys():
##    normal_dist[key]=float(degree_dict[key])/len(citation_graph)


##z = sorted(normal_dist)
##
##
##x = z[1:]
##y = [normal_dist[i] for i in x]
##
##
##fig = plt.figure()
##fig.suptitle('Degree Distribution')
##ax = fig.add_subplot(111)
##ax.set_xlabel('in-degree')
##ax.set_ylabel('percentage')
##ax.loglog(x,y)
##ax.grid(True)
##plt.show()


"""
Provided code for application portion of module 1

Helper class for implementing efficient version
of DPA algorithm
"""

# general imports
import random


class DPATrial:
    """
    Simple class to encapsulate optimized trials for DPA algorithm
    
    Maintains a list of node numbers with multiple instances of each number.
    The number of instances of each node number are
    in the same proportion as the desired probabilities
    
    Uses random.choice() to select a node number from this list for each trial.
    """

    def __init__(self, num_nodes):
        """
        Initialize a DPATrial object corresponding to a 
        complete graph with num_nodes nodes
        
        Note the initial list of node numbers has num_nodes copies of
        each node number
        """
        self._num_nodes = num_nodes
        self._node_numbers = [node for node in range(num_nodes) for dummy_idx in range(num_nodes)]


    def run_trial(self, num_nodes):
        """
        Conduct num_node trials using by applying random.choice()
        to the list of node numbers
        
        Updates the list of node numbers so that the number of instances of
        each node number is in the same ratio as the desired probabilities
        
        Returns:
        Set of nodes
        """
        
        # compute the neighbors for the newly-created node
        new_node_neighbors = set()
        for dummy_idx in range(num_nodes):
            new_node_neighbors.add(random.choice(self._node_numbers))
        
        # update the list of node numbers so that each node number 
        # appears in the correct ratio
        self._node_numbers.append(self._num_nodes)
        self._node_numbers.extend(list(new_node_neighbors))
        
        #update the number of nodes
        self._num_nodes += 1
        return new_node_neighbors

    def get_num_nodes(self):
        return self._num_nodes

import collections    
def DPA(n,m):
    node_holder = DPATrial(m)
    for dummy_idx in range(n-m):
        node_holder.run_trial(m)
##    return node_holder
    DPA_in_degrees = collections.Counter(node_holder._node_numbers)
    return collections.Counter(DPA_in_degrees.values())
    return DPA_in_degrees

graph = DPA(27770,12)




normal_dist = {}
for key in graph.keys():
    normal_dist[key]=float(graph[key])/len(graph)


z = sorted(normal_dist)
##
##
x = z[1:]
y = [normal_dist[i] for i in x]
##
##
fig = plt.figure()
fig.suptitle('DPA Degree Distribution')
ax = fig.add_subplot(111)
ax.set_xlabel('in-degree')
ax.set_ylabel('percentage')
ax.loglog(x,y)
ax.grid(True)
plt.show()
    

    

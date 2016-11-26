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

            
    

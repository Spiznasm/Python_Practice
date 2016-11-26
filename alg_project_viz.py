"""
Example code for creating and visualizing
cluster of county-based cancer risk data

Note that you must download the file
http://www.codeskulptor.org/#alg_clusters_matplotlib.py
to use the matplotlib version of this code
"""

# Flavor of Python - desktop or CodeSkulptor
DESKTOP = True

import math
import random
import urllib2
import alg_cluster
import matplotlib.pyplot as plt

# conditional imports
if DESKTOP:
    import Checked as alg_project3_solution      # desktop project solution
    import alg_clusters_matplotlib
else:
    #import userXX_XXXXXXXX as alg_project3_solution   # CodeSkulptor project solution
    import alg_clusters_simplegui
    import codeskulptor
    codeskulptor.set_timeout(30)


###################################################
# Code to load data tables

# URLs for cancer risk data tables of various sizes
# Numbers indicate number of counties in data table

DIRECTORY = "http://commondatastorage.googleapis.com/codeskulptor-assets/"
DATA_3108_URL = DIRECTORY + "data_clustering/unifiedCancerData_3108.csv"
DATA_896_URL = DIRECTORY + "data_clustering/unifiedCancerData_896.csv"
DATA_290_URL = DIRECTORY + "data_clustering/unifiedCancerData_290.csv"
DATA_111_URL = DIRECTORY + "data_clustering/unifiedCancerData_111.csv"


def load_data_table(data_url):
    """
    Import a table of county-based cancer risk data
    from a csv format file
    """
    data_file = urllib2.urlopen(data_url)
    data = data_file.read()
    data_lines = data.split('\n')
    print "Loaded", len(data_lines), "data points"
    data_tokens = [line.split(',') for line in data_lines]
    return [[tokens[0], float(tokens[1]), float(tokens[2]), int(tokens[3]), float(tokens[4])]
            for tokens in data_tokens]


############################################################
# Code to create sequential clustering
# Create alphabetical clusters for county data

def sequential_clustering(singleton_list, num_clusters):
    """
    Take a data table and create a list of clusters
    by partitioning the table into clusters based on its ordering

    Note that method may return num_clusters or num_clusters + 1 final clusters
    """

    cluster_list = []
    cluster_idx = 0
    total_clusters = len(singleton_list)
    cluster_size = float(total_clusters)  / num_clusters

    for cluster_idx in range(len(singleton_list)):
        new_cluster = singleton_list[cluster_idx]
        if math.floor(cluster_idx / cluster_size) != \
           math.floor((cluster_idx - 1) / cluster_size):
            cluster_list.append(new_cluster)
        else:
            cluster_list[-1] = cluster_list[-1].merge_clusters(new_cluster)

    return cluster_list


#####################################################################
# Code to load cancer data, compute a clustering and
# visualize the results


def run_example():
    """
    Load a data table, compute a list of clusters and
    plot a list of clusters

    Set DESKTOP = True/False to use either matplotlib or simplegui
    """
    data_table = load_data_table(DATA_111_URL)

    singleton_list = []
    for line in data_table:
        singleton_list.append(alg_cluster.Cluster(set([line[0]]), line[1], line[2], line[3], line[4]))

    #cluster_list = sequential_clustering(singleton_list, 15)
    #print "Displaying", len(cluster_list), "sequential clusters"

    #cluster_list = alg_project3_solution.hierarchical_clustering(singleton_list, 9)
    #print "Displaying", len(cluster_list), "hierarchical clusters"

    cluster_list = alg_project3_solution.kmeans_clustering(singleton_list, 9, 5)
    print "Displaying", len(cluster_list), "k-means clusters"


    # draw the clusters using matplotlib or simplegui
    if DESKTOP:
        alg_clusters_matplotlib.plot_clusters(data_table, cluster_list, True)
        #alg_clusters_matplotlib.plot_clusters(data_table, cluster_list, True)  #add cluster centers
    else:
        alg_clusters_simplegui.PlotClusters(data_table, cluster_list)   # use toggle in GUI to add cluster centers

#run_example()

def compute_distortion(cluster_list,data_table):
    

    distortion = 0
    for cluster in cluster_list:
        distortion += cluster.cluster_error(data_table)
    return distortion

data_table111 = load_data_table(DATA_111_URL)
data_table290 = load_data_table(DATA_290_URL)
data_table896 = load_data_table(DATA_896_URL)

singleton_list = []
for line in data_table111:
    singleton_list.append(alg_cluster.Cluster(set([line[0]]), line[1], line[2], line[3], line[4]))

doubleton_list = []
for line in data_table290:
    doubleton_list.append(alg_cluster.Cluster(set([line[0]]), line[1], line[2], line[3], line[4]))

octaton_list = []
for line in data_table896:
    octaton_list.append(alg_cluster.Cluster(set([line[0]]), line[1], line[2], line[3], line[4]))

distortion_111_h = []
distortion_290_h = []
distortion_896_h = []
distortion_111_k = []
distortion_290_k = []
distortion_896_k = []
for cluster_size in range(6,21):
    distortion_111_h.append(compute_distortion(alg_project3_solution.hierarchical_clustering(singleton_list, cluster_size),data_table111))
    distortion_111_k.append(compute_distortion(alg_project3_solution.kmeans_clustering(singleton_list, cluster_size, 5),data_table111))
    distortion_290_h.append(compute_distortion(alg_project3_solution.hierarchical_clustering(doubleton_list, cluster_size),data_table290))
    distortion_290_k.append(compute_distortion(alg_project3_solution.kmeans_clustering(doubleton_list, cluster_size, 5),data_table290))
    distortion_896_h.append(compute_distortion(alg_project3_solution.hierarchical_clustering(octaton_list, cluster_size),data_table896))
    distortion_896_k.append(compute_distortion(alg_project3_solution.kmeans_clustering(octaton_list, cluster_size, 5),data_table896))

def graph111():
    xvals = range(6,21)
    yvals1 = distortion_111_h
    yvals2 = distortion_111_k
    #yvals3 = upa_resilience

    plt.xlabel("Number of Clusters")
    plt.ylabel("Distortion")
    plt.title("Hierarchical vs K-means on the DATA_111 table")
    plt.plot(xvals, yvals1, '-b', label='Hierarchical')
    plt.plot(xvals, yvals2, '-r', label='K-means')
    #plt.plot(xvals, yvals3, '-g', label='upa graph m=2')
    plt.legend(loc='upper right')
    plt.show()

def graph290():
    xvals = range(6,21)
    yvals1 = distortion_111_h
    yvals2 = distortion_111_k
    #yvals3 = upa_resilience

    plt.xlabel("Number of Clusters")
    plt.ylabel("Distortion")
    plt.title("Hierarchical vs K-means on the DATA_290 table")
    plt.plot(xvals, yvals1, '-b', label='Hierarchical')
    plt.plot(xvals, yvals2, '-r', label='K-means')
    #plt.plot(xvals, yvals3, '-g', label='upa graph m=2')
    plt.legend(loc='upper right')
    plt.show()

def graph896():
    xvals = range(6,21)
    yvals1 = distortion_111_h
    yvals2 = distortion_111_k
    #yvals3 = upa_resilience

    plt.xlabel("Number of Clusters")
    plt.ylabel("Distortion")
    plt.title("Hierarchical vs K-means on the DATA_896 table")
    plt.plot(xvals, yvals1, '-b', label='Hierarchical')
    plt.plot(xvals, yvals2, '-r', label='K-means')
    #plt.plot(xvals, yvals3, '-g', label='upa graph m=2')
    plt.legend(loc='upper right')
    plt.show()

"""
Cluster class for Module 3
"""

import math
import random
from time import time
import matplotlib.pyplot as plt

class Cluster:
    """
    Class for creating and merging clusters of counties
    """

    def __init__(self, fips_codes, horiz_pos, vert_pos, population, risk):
        """
        Create a cluster based the models a set of counties' data
        """
        self._fips_codes = fips_codes
        self._horiz_center = horiz_pos
        self._vert_center = vert_pos
        self._total_population = population
        self._averaged_risk = risk


    def __repr__(self):
        """
        String representation assuming the module is "alg_cluster".
        """
        rep = "alg_cluster.Cluster("
        rep += str(self._fips_codes) + ", "
        rep += str(self._horiz_center) + ", "
        rep += str(self._vert_center) + ", "
        rep += str(self._total_population) + ", "
        rep += str(self._averaged_risk) + ")"
        return rep


    def fips_codes(self):
        """
        Get the cluster's set of FIPS codes
        """
        return self._fips_codes

    def horiz_center(self):
        """
        Get the averged horizontal center of cluster
        """
        return self._horiz_center

    def vert_center(self):
        """
        Get the averaged vertical center of the cluster
        """
        return self._vert_center

    def total_population(self):
        """
        Get the total population for the cluster
        """
        return self._total_population

    def averaged_risk(self):
        """
        Get the averaged risk for the cluster
        """
        return self._averaged_risk


    def copy(self):
        """
        Return a copy of a cluster
        """
        copy_cluster = Cluster(set(self._fips_codes), self._horiz_center, self._vert_center,
                               self._total_population, self._averaged_risk)
        return copy_cluster


    def distance(self, other_cluster):
        """
        Compute the Euclidean distance between two clusters
        """
        vert_dist = self._vert_center - other_cluster.vert_center()
        horiz_dist = self._horiz_center - other_cluster.horiz_center()
        return math.sqrt(vert_dist ** 2 + horiz_dist ** 2)

    def merge_clusters(self, other_cluster):
        """
        Merge one cluster into another
        The merge uses the relatively populations of each
        cluster in computing a new center and risk

        Note that this method mutates self
        """
        if len(other_cluster.fips_codes()) == 0:
            return self
        else:
            self._fips_codes.update(set(other_cluster.fips_codes()))

            # compute weights for averaging
            self_weight = float(self._total_population)
            other_weight = float(other_cluster.total_population())
            self._total_population = self._total_population + other_cluster.total_population()
            self_weight /= self._total_population
            other_weight /= self._total_population

            # update center and risk using weights
            self._vert_center = self_weight * self._vert_center + other_weight * other_cluster.vert_center()
            self._horiz_center = self_weight * self._horiz_center + other_weight * other_cluster.horiz_center()
            self._averaged_risk = self_weight * self._averaged_risk + other_weight * other_cluster.averaged_risk()
            return self

    def cluster_error(self, data_table):
        """
        Input: data_table is the original table of cancer data used in creating the cluster.

        Output: The error as the sum of the square of the distance from each county
        in the cluster to the cluster center (weighted by its population)
        """
        # Build hash table to accelerate error computation
        fips_to_line = {}
        for line_idx in range(len(data_table)):
            line = data_table[line_idx]
            fips_to_line[line[0]] = line_idx

        # compute error as weighted squared distance from counties to cluster center
        total_error = 0
        counties = self.fips_codes()
        for county in counties:
            line = data_table[fips_to_line[county]]
            singleton_cluster = Cluster(set([line[0]]), line[1], line[2], line[3], line[4])
            singleton_distance = self.distance(singleton_cluster)
            total_error += (singleton_distance ** 2) * singleton_cluster.total_population()
        return total_error



def slow_closest_pair(cluster_list):
    """Returns the closest clusters listing the earliest index first"""
    closest = (float('inf'),-1,-1)
    cluster_index = range(len(cluster_list))
    for idx in cluster_index:
        cluster_one = cluster_list[idx]
        other_clusters = cluster_index[:idx]+cluster_index[idx+1:]
        for other_idx in other_clusters:
            cluster_two = cluster_list[other_idx]
            distance = cluster_one.distance(cluster_two)
            if distance < closest[0] and idx < other_idx:
                closest = (distance,idx,other_idx)
    return closest

def closest_pair_strip(cluster_list,horiz_center,half_width):
    """Helper Function for fast_closest_pair returns the closest pair that are both half_width away from horiz_center"""
    viable_clusters = []
    for cluster in cluster_list:
        if math.fabs(cluster.horiz_center()-horiz_center)<half_width:
            viable_clusters.append(cluster)
    viable_clusters.sort(key=lambda cluster: cluster.vert_center())
    cluster_count = len(viable_clusters)
    closest = (float('inf'),-1,-1)
    for idx in range(0,cluster_count-1):
        parent_idx = cluster_list.index(viable_clusters[idx])

        for other_idx in range(idx+1,min(idx+4,cluster_count)):
            other_parent_idx = cluster_list.index(viable_clusters[other_idx])

            distance_between = viable_clusters[idx].distance(viable_clusters[other_idx])
            if parent_idx > other_parent_idx:
                possible_closest = (distance_between,other_parent_idx,parent_idx)
            else:
                possible_closest = (distance_between,parent_idx,other_parent_idx)
            closest = min(closest,possible_closest)

    return closest


def fast_closest_pair(cluster_list):
    """Returns closest pair of clusters in the list by divide and conquer"""
    list_size = len(cluster_list)
    if list_size <= 3:
        closest=slow_closest_pair(cluster_list)
    else:
        half_list_size = list_size/2
        left_list = cluster_list[:half_list_size]
        right_list = cluster_list[half_list_size:]
        left_closest = fast_closest_pair(left_list)
        right_closest = fast_closest_pair(right_list)
        closest = min(left_closest,(right_closest[0],right_closest[1]+half_list_size,right_closest[2]+half_list_size))
        center = 0.5*(cluster_list[half_list_size-1].horiz_center()+cluster_list[half_list_size].horiz_center())
        closest = min(closest,closest_pair_strip(cluster_list,center,closest[0]))
    return closest

def hierarchical_clustering(cluster_list, num_clusters):
    """Groups the clusters in cluster_list into num_clusters clusters"""
    final_clusters = cluster_list

    while len(final_clusters) > num_clusters:
        final_clusters.sort(key = lambda cluster: cluster.horiz_center())
        merge_pair = fast_closest_pair(final_clusters)
        merge_cluster_one = final_clusters[merge_pair[1]]
        merge_cluster_two = final_clusters[merge_pair[2]]
        merge_cluster_one.merge_clusters(merge_cluster_two)
        final_clusters.remove(merge_cluster_two)
    return final_clusters

def distance_formula(coordinate_one,coordinate_two):
    """helpr function to find distance between two points"""
    xdiff = coordinate_two[0]-coordinate_one[0]
    ydiff = coordinate_two[1]-coordinate_one[1]
    distance = math.sqrt(xdiff**2+ydiff**2)
    return distance



def kmeans_clustering(cluster_list, num_clusters, num_iterations):
     """Groups the clusters in cluster_list into num_clusters by interating num_iterations"""

     cluster_copies = [dummy_cluster.copy() for dummy_cluster in cluster_list]
     cluster_copies.sort(key = lambda cluster_list: cluster_list.total_population(), reverse = True)
     # position initial clusters at the location of clusters with largest populations
     centers = [dummy_cluster for dummy_cluster in cluster_copies[:num_clusters]]
     for dummy_iter in range(num_iterations):
         final_clusters = [[] for dummy_id in range(num_clusters)]
         for cluster_idx in range(len(cluster_list)):
             distance = float('inf')
             for center_idx in range(num_clusters):
                 if cluster_list[cluster_idx].distance(centers[center_idx]) < distance:
                     distance = cluster_list[cluster_idx].distance(centers[center_idx])
                     chosen_center = center_idx
             if final_clusters[chosen_center] == []:
                 final_clusters[chosen_center] = cluster_list[cluster_idx].copy()
             else:
                 final_clusters[chosen_center].merge_clusters(cluster_list[cluster_idx])
         for center_idx in range(num_clusters):
             centers[center_idx] = final_clusters[center_idx].copy()

     return final_clusters

def gen_random_clusters(num_clusters):
    random_clusters = []
    for dummy_var in range(num_clusters):
        cluster = Cluster(set([]),random.uniform(-1,1),random.uniform(-1,1),0,0)
        random_clusters.append(cluster)
    return random_clusters

def gen_cluster_lists(smallest,largest):
    cluster_lists = []
    for dummy_var in range(smallest,largest+1):
        random_list = gen_random_clusters(dummy_var)
        cluster_lists.append(random_list)
    return cluster_lists

def slow_data(dataset):
    data_list = []
    for data in dataset:
        start = time()
        slow_closest_pair(data)
        stop = time()
        data_list.append(stop-start)
    return data_list

def fast_data(dataset):
    data_list = []
    for data in dataset:
        start = time()
        fast_closest_pair(data)
        stop = time()
        data_list.append(stop-start)
    return data_list

def graph():
    xvals = range(2,201)
    yvals1 = slow_data(gen_cluster_lists(2,200))
    yvals2 = fast_data(gen_cluster_lists(2,200))
    #yvals3 = upa_resilience

    plt.xlabel("Number of Clusters")
    plt.ylabel("Runtime")
    plt.title("Slow vs. Fast Closest Pair")
    plt.plot(xvals, yvals1, '-b', label='slow')
    plt.plot(xvals, yvals2, '-r', label='fast')
    #plt.plot(xvals, yvals3, '-g', label='upa graph m=2')
    plt.legend(loc='upper right')
    plt.show()

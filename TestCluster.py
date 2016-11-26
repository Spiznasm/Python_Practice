"""
Cluster class for Module 3
"""

import math


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
    viable_clusters = []
    for cluster in cluster_list:
        if math.fabs(cluster.horiz_center()-horiz_center)<half_width:
            viable_clusters.append(cluster)
    print len(cluster_list),len(viable_clusters)
    viable_clusters.sort(key=lambda cluster: cluster.vert_center())
    print viable_clusters
    cluster_count = len(viable_clusters)
    closest = (float('inf'),-1,-1)
    for idx in range(0,cluster_count-1):
        parent_idx = cluster_list.index(viable_clusters[idx])
        parent_cluster = cluster_list[parent_idx]
        for other_idx in range(idx+1,min(idx+3,cluster_count)):
            print idx,other_idx
            other_parent_idx = cluster_list.index(viable_clusters[other_idx])
            other_parent_cluster = cluster_list[other_parent_idx]
            distance_between = viable_clusters[idx].distance(viable_clusters[other_idx])
            print distance_between
            if parent_idx > other_parent_idx:
                possible_closest = (distance_between,other_parent_idx,parent_idx)
            else:
                possible_closest = (distance_between,parent_idx,other_parent_idx)
            print closest,possible_closest
            closest = min(closest,possible_closest)
            
            print closest
    return closest


def fast_closest_pair(cluster_list):
    list_size = len(cluster_list)
    if list_size <= 3:
        slow_closest_pair(cluster_list)
    else:
        half_list_size = list_size/2
        left_list = cluster_list[:half_list_size]
        right_list = cluster_list[half_list_size:]
        left_closest = fast_closest_pair(left_list)
        right_closest = fast_closest_pair(right_list)
        closest = min(left_closest,(right_closest[0],right_closest[1]+half_list_size,right_closest[2]+half_list_size))
        center = 0.5*(cluster_list[half_list_size-1].horiz_center()+cluster_list[half_list_size].horiz_center())
        closest = min(closest,closest_pair_strip(cluster_list,center,center[0]))
    return closest


a = Cluster(set([]), 0, 0, 1, 0)
b = Cluster(set([]), 0, 1, 1, 0)
c = Cluster(set([]), 1, 0, 1, 0)
d = Cluster(set([]), 1, 1, 1, 0)
e = Cluster(set([]), -4.0,0.0,1,0)
f = Cluster(set([]), 0.0,-1.0,1,0)
g = Cluster(set([]), 0.0,1.0,1,0)
h = Cluster(set([]), 4.0,0.0,1,0)

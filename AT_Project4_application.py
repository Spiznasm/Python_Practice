"""
Provide code and solution for Application 4
"""

DESKTOP = True

import math
import random
import urllib2


if DESKTOP:
    import matplotlib.pyplot as plt
    import AT_Project4_Functions as student
else:
    import simpleplot
    import userXX_XXXXXXX as student


# URLs for data files
PAM50_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_PAM50.txt"
HUMAN_EYELESS_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_HumanEyelessProtein.txt"
FRUITFLY_EYELESS_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_FruitflyEyelessProtein.txt"
CONSENSUS_PAX_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_ConsensusPAXDomain.txt"
WORD_LIST_URL = "http://storage.googleapis.com/codeskulptor-assets/assets_scrabble_words3.txt"



###############################################
# provided code

def read_scoring_matrix(filename):
    """
    Read a scoring matrix from the file named filename.

    Argument:
    filename -- name of file containing a scoring matrix

    Returns:
    A dictionary of dictionaries mapping X and Y characters to scores
    """
    scoring_dict = {}
    scoring_file = urllib2.urlopen(filename)
    ykeys = scoring_file.readline()
    ykeychars = ykeys.split()
    for line in scoring_file.readlines():
        vals = line.split()
        xkey = vals.pop(0)
        scoring_dict[xkey] = {}
        for ykey, val in zip(ykeychars, vals):
            scoring_dict[xkey][ykey] = int(val)
    return scoring_dict




def read_protein(filename):
    """
    Read a protein sequence from the file named filename.

    Arguments:
    filename -- name of file containing a protein sequence

    Returns:
    A string representing the protein
    """
    protein_file = urllib2.urlopen(filename)
    protein_seq = protein_file.read()
    protein_seq = protein_seq.rstrip()
    return protein_seq


def read_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    # load assets
    word_file = urllib2.urlopen(filename)

    # read in files as string
    words = word_file.read()

    # template lines and solution lines list of line string
    word_list = words.split('\n')
    print "Loaded a dictionary with", len(word_list), "words"
    return word_list

human_eyeless = read_protein(HUMAN_EYELESS_URL)
fruitfly_eyeless = read_protein(FRUITFLY_EYELESS_URL)
q1_score_grid = read_scoring_matrix(PAM50_URL)
q1_alignment_matrix = student.compute_alignment_matrix(human_eyeless,fruitfly_eyeless,q1_score_grid,False)
q1_answer = student.compute_local_alignment(human_eyeless,fruitfly_eyeless,q1_score_grid,q1_alignment_matrix)
# print q1_answer
#
human_seq = q1_answer[1]
fly_seq = q1_answer[2]
# human_seq = human_seq.translate(None,'-')
# fly_seq = fly_seq.translate(None,'-')
# concensus = read_protein(CONSENSUS_PAX_URL)
# q2_human_grid = student.compute_alignment_matrix(human_seq,concensus,q1_score_grid,True)
# q2_fly_grid = student.compute_alignment_matrix(fly_seq,concensus,q1_score_grid,True)
# q2_human_answer = student.compute_global_alignment(human_seq,concensus,q1_score_grid,q2_human_grid)
# q2_fly_answer = student.compute_global_alignment(fly_seq,concensus,q1_score_grid,q2_fly_grid)
# for mem in q2_human_answer:
#     print mem
# for mem in q2_fly_answer:
#     print mem
# fly_matching = 0
# fly_total = 0
# human_matching = 0
# human_total = 0
# global_fly = q2_fly_answer[1]
# fly_con = q2_fly_answer[2]
# human_con = q2_human_answer[2]
# global_human = q2_human_answer[1]
# for idx in range(len(global_fly)):
#     fly_total += 1
#     if global_fly[idx] == fly_con[idx]:
#         fly_matching += 1
# for idx in range(len(global_human)):
#     human_total += 1
#     if global_human[idx] == human_con[idx]:
#         human_matching += 1
# print float(human_matching)/human_total
# print float(fly_matching)/fly_total

def generate_null_distribution(seq_x, seq_y, scoring_matrix, num_trials):
    scoring_distribution = {}
    #calculated_alignment_matrix = student.compute_alignment_matrix(seq_x,seq_y,scoring_matrix,False)
    for dummy_trial in range(num_trials):
        rand_y = ''.join(random.sample(seq_y,len(seq_y)))
        score = student.compute_local_alignment(seq_x,rand_y,scoring_matrix,student.compute_alignment_matrix(seq_x,rand_y,scoring_matrix,False))[0]
        if score in scoring_distribution:
            scoring_distribution[score]+=1
        else:
            scoring_distribution[score]=1
    return scoring_distribution

q4_scores = generate_null_distribution(human_eyeless,fruitfly_eyeless,q1_score_grid,1000)

q4_x_values = q4_scores.keys()
q4_x_values.sort()
q4_y_values = []
for key in q4_x_values:
    q4_y_values.append(q4_scores[key]/float(1000))
#print sum(q4_y_values)
plt.bar(q4_x_values,q4_y_values)
plt.ylabel('Score Frequency')
plt.xlabel('Score')
plt.title('Score distribution of random sequences')
plt.show()
#
# average = sum(q4_x_values)/float(1000)
# differences = []
# for value in q4_x_values:
#     differences.append((value-average)**2)
# std_dev = math.sqrt(sum(differences)/float(1000))
# human_z_score = (0.729323308271-average)/float(std_dev)
# fly_z_score = (0.701492537313-average)/float(std_dev)
# print average,std_dev,human_z_score,fly_z_score

##def check_spelling(checked_word,dist,word_list):
##    score_matrix = student.build_scoring_matrix('abcdefghijklmnopqrstuvwxyz',2,1,0)
##    matching_words = []
##    for word in word_list:
##        global_answer = student.compute_global_alignment(checked_word,word,score_matrix,student.compute_alignment_matrix(checked_word,word,score_matrix,True))
##        global_align_score = global_answer[0]
##        if len(checked_word)+len(word)-global_align_score <= dist:
##            matching_words.append(word)
##    return matching_words
##
##possible_words = read_words(WORD_LIST_URL)
##score_matrix = student.build_scoring_matrix('abcdefghijklmnopqrstuvwxyz',2,1,0)
###print score_matrix
##humble_list = check_spelling('humble',1,possible_words)
##firefly_list = check_spelling('firefly',2,possible_words)
##print humble_list
##print firefly_list

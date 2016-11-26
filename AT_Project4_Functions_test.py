"""Functions to use dynamic programming in measuring the similarity between two sequences of characters."""

def build_scoring_matrix(alphabet, diag_score, off_diag_score, dash_score):
    """Builds a scoring matrix that sets pairs with a dash to dash_score, equal pairs to diag_score, and unequal scores to off_diag_score"""
    mod_alphabet = set(alphabet)
    mod_alphabet.add('-')
    parent_dict = {}
    for out_letter in mod_alphabet:
        parent_dict[out_letter]=dict()
        for in_letter in mod_alphabet:
            if out_letter=='-' or in_letter == '-':
                parent_dict[out_letter][in_letter]=dash_score
            elif out_letter == in_letter:
                parent_dict[out_letter][in_letter]=diag_score
            else:
                parent_dict[out_letter][in_letter]=off_diag_score
    return parent_dict

def compute_alignment_matrix(seq_x, seq_y, scoring_matrix, global_flag):
    """Creates a list of lists that represents the alignment matrix.  global_flag = False for local alignment matris"""
    alignment_matrix = []
    for row in range(len(seq_x)+1):
        alignment_matrix.append([])
    for row in range(len(seq_x)+1):
        for dummy_col in range(len(seq_y)+1):
            alignment_matrix[row].append(0)

    for dummy_idx in range(1,len(seq_x)+1):
        s_i_0 = alignment_matrix[dummy_idx-1][0] + scoring_matrix[seq_x[dummy_idx - 1]]['-']
        if s_i_0 < 0 and global_flag == False:
            s_i_0 = 0
        alignment_matrix[dummy_idx][0]=s_i_0
    for dummy_idx in range(1,len(seq_y)+1):
        s_0_j = alignment_matrix[0][dummy_idx-1] + scoring_matrix['-'][seq_y[dummy_idx - 1]]
        if s_0_j < 0 and global_flag == False:
            s_0_j = 0
        alignment_matrix[0][dummy_idx]=s_0_j
    for x_idx in range(1,len(seq_x)+1):
        for y_idx in range(1,len(seq_y)+1):
            option1 = alignment_matrix[x_idx - 1][y_idx - 1] + scoring_matrix[seq_x[x_idx - 1]][seq_y[y_idx - 1]]
            option2 = alignment_matrix[x_idx - 1][y_idx] + scoring_matrix[seq_x[x_idx - 1]]['-']
            option3 = alignment_matrix[x_idx][y_idx - 1] + scoring_matrix['-'][seq_y[y_idx - 1]]
            alignment_matrix[x_idx][y_idx] = max(option1,option2,option3)
            if global_flag == False and alignment_matrix[x_idx][y_idx] < 0:
                alignment_matrix[x_idx][y_idx] = 0
    return alignment_matrix

def compute_global_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):
    """Returns a tuple of the form (score,aligned x, aligned y) where aligned x and aligned y are the best alignment of seq_x and seq_y"""
    x_pos = len(seq_x)
    y_pos = len(seq_y)
    new_x_seq = ""
    new_y_seq = ""
    while x_pos!=0 and y_pos!=0:
        if alignment_matrix[x_pos][y_pos]==alignment_matrix[x_pos - 1][y_pos - 1] + scoring_matrix[seq_x[x_pos -1]][seq_y[y_pos -1]]:
            new_x_seq = seq_x[x_pos - 1] + new_x_seq
            new_y_seq = seq_y[y_pos - 1] + new_y_seq
            x_pos -=1
            y_pos -=1
        else:
            if alignment_matrix[x_pos][y_pos] == alignment_matrix[x_pos-1][y_pos]+scoring_matrix[seq_x[x_pos-1]]['-']:
                new_x_seq = seq_x[x_pos - 1] + new_x_seq
                new_y_seq = '-' + new_y_seq
                x_pos-=1
            else:
                new_x_seq ='-'+new_x_seq
                new_y_seq =seq_y[y_pos-1]+new_y_seq
                y_pos -=1
    while x_pos != 0:
        new_x_seq=seq_x[x_pos-1]+new_x_seq
        new_y_seq='-'+ new_y_seq
        x_pos -=1
    while y_pos !=0:
        new_x_seq='-'+ new_x_seq
        new_y_seq=seq_y[y_pos -1]+new_y_seq
        y_pos -=1
    seq_score = 0
    for dummy_idx in range(len(new_x_seq)):
        seq_score += scoring_matrix[new_x_seq[dummy_idx]][new_y_seq[dummy_idx]]
    return (seq_score,new_x_seq,new_y_seq)


def compute_local_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):
    max_score = -float('inf')
    for row in range(len(alignment_matrix)):
        for col in range(len(alignment_matrix[0])):
            if alignment_matrix[row][col]>max_score:
                max_score = alignment_matrix[row][col]
                start_x = row
                start_y = col

    x_pos = start_x
    y_pos = start_y
    new_x_seq = ""
    new_y_seq = ""
    while x_pos!=0 and y_pos!=0:
    #while alignment_matrix[x_pos][y_pos]!=0:
        if alignment_matrix[x_pos - 1][y_pos - 1] == 0:
            break
        elif alignment_matrix[x_pos][y_pos]==alignment_matrix[x_pos - 1][y_pos - 1] + scoring_matrix[seq_x[x_pos -1]][seq_y[y_pos -1]]:
            new_x_seq = seq_x[x_pos - 1] + new_x_seq
            new_y_seq = seq_y[y_pos - 1] + new_y_seq
            x_pos -=1
            y_pos -=1
        else:
            if alignment_matrix[x_pos-1][y_pos] == 0:
                break
            elif alignment_matrix[x_pos][y_pos] == alignment_matrix[x_pos-1][y_pos]+scoring_matrix[seq_x[x_pos-1]]['-']:
                new_x_seq = seq_x[x_pos - 1] + new_x_seq
                new_y_seq = '-' + new_y_seq
                x_pos-=1
            elif alignment_matrix[x_pos][y_pos-1]:
                break
            else:
                new_x_seq ='-'+new_x_seq
                new_y_seq =seq_y[y_pos-1]+new_y_seq
                y_pos -=1
    while x_pos != 0:
        new_x_seq=seq_x[x_pos-1]+new_x_seq
        new_y_seq='-'+ new_y_seq
        x_pos -=1
    while y_pos !=0:
        new_x_seq='-'+ new_x_seq
        new_y_seq=seq_y[y_pos -1]+new_y_seq
        y_pos -=1
    seq_score = 0
    for dummy_idx in range(len(new_x_seq)):
        seq_score += scoring_matrix[new_x_seq[dummy_idx]][new_y_seq[dummy_idx]]
    return (seq_score,new_x_seq,new_y_seq)

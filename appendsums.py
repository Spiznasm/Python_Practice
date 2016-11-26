def appendsums(list):
    for num in range(25):
        new_sum = sum(list[-3:])
        list.append(new_sum)
        

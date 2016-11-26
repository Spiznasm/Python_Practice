def merge(line):
    zeroes = 0
    reordered = []
    combined = []
    skip = False
    for num in line:
        if num == 0:
            zeroes +=1
        else:
            reordered.append(num)
    for num in range(zeroes):
        reordered.append(0)

    zeroes = 0

    for num in range(len(reordered)):
        try:
            if skip == True:
                skip = False
                continue
            else:
                if reordered[num] == 0:
                    zeroes +=1
                elif reordered[num] == reordered[num+1]:
                    combined.append(reordered[num]*2)
                    zeroes +=1
                    skip = True
                else:
                    combined.append(reordered[num])

        except IndexError:
            combined.append(reordered[num])

    for num in range(zeroes):
        combined.append(0)

    return combined
        
            
        

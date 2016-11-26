import re
doc = raw_input("File Name: ")
hand = open(doc)
numbers = []
count = 0
total = 0
for line in hand:
    x = re.findall('[0-9]+',line)
    numbers += x
    count += len(x)

for num in numbers:
    total += int(num)

print "There are "+str(count)+" numbers, that total "+str(total)+" ."

    
    

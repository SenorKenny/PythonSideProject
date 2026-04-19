hundo=3

while hundo<100:
    print (hundo)
    hundo +=3


import time
count=input("Choose a number great than or equal to 1 to countdown from 0: ")
count_int=int(count)
while count_int > 0:
    print(count_int)
    time.sleep(.1)
    count_int -= 1
print("Lets go!!!!")
#To do list
#Will make a while loop that asks user for input
#break the loop will cause it to print everything that's been store so far.

to_do=[]
answer=input("Would you like to add to your to-do list? (y/n) ").lower()

while answer == "y" or answer == "yes":
    x=input ("What would you like to add? ")
    to_do.append(x)
    answer=input("Continue? (y/n) ").lower()

for tasks in to_do:
    print(tasks)
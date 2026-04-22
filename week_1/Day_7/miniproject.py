# Will simulatee a task inputer


num_task=input("How many to-do activities  you want to list today? ")


def task_adder(numberoftasks):
    random_list=[]
    if type(numberoftasks) == str:
        numberoftasks=int(numberoftasks)
    for x in range(numberoftasks):
        random_list.append(input("What tasks do you want to list? "))
    return random_list

def task_printer(tasklist):
    print("\n Your tasks today are: ")
    for x in range(len(tasklist)):
        print(tasklist[x])
def task_processor(sametaxlist):
    i=0
    while i<len(sametaxlist):
        print(f"Processing the following task: {sametaxlist[i]}")
        i+=1

our_new_list=task_adder(num_task)
print(len(our_new_list))

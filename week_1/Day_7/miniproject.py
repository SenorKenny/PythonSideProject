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
    with open("NewTasks.txt",'w') as file:
        file.write("Your tasks today are")
    
    with open("NewTasks.txt", 'a') as file:
            for x in range(len(tasklist)):
                file.write("\n"+tasklist[x])

def task_processor(sametaxlist):
    i=0
    while i<len(sametaxlist):
        print(f"Processing the following task: {sametaxlist[i]}")
        i+=1

our_new_list=task_adder(num_task)
task_printer(our_new_list)
task_processor(our_new_list)
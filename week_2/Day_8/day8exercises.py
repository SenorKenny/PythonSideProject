

#task 1 , writing a function that takes a file name as an input, and creates or 
# writes to said file. All while asking how many inputs you want to add
def writing(filename):
    with open(filename, 'w') as file:
        tasks=int(input("How many tasks do you want to input? "))
        for x in range(tasks):
            
            file.write(input(f"write task {x+1}: ")+"\n")

#practcing opening and closing without 'with'
def printfile(filename):
    f=open(filename)
    print(f.read())
    f.close
    
def file2list(filename):
    newlist=[]
    with open(filename) as file:
            for line in file:
                newlist.append(line)
    return newlist



writing("test.txt")
printfile("test.txt")
testlist=file2list("test.txt")
print(testlist)


#task 1 . Function greet and print

def greet():
    print("Hello!")

greet()

#task 2 . Greet_user with parameter

def greet_user(name):
    print(f"Hello {name}")

greet_user("Arnold")


#Task 3. Make function that adds 2 integers

def Addition_calc(a,b):
    return a+b

print(Addition_calc(3,10))

#Task 4, even cheecker for integer

def even_checker(var):
    var=int(var)
    if var%2 ==0:
        return "even"
    else:
        return "odd"

var=input("Enter a number ")
print(even_checker(var))

#Task 5, usename formatter

def username_formatter(name):
    return name.lower().replace(" ","")
print(username_formatter("Amy Weiner"))

#task 6
def multi(a,b):
    return a*b
def divide(a,b):
    return a/b

multi(5,10)
divide(40,8)

#My harder attempt?

x=[]
snack="1"
def func1():
    snack=input("How many snacks do you want to list? ")
    return snack
    
def func2(dainput): #assigns each printable statement as a list 
    for num in range(int(dainput)):
        x.append(input("what is you favorite snack? "))
    return x

def func3(daresults):
    print(f"Your favorite snacks are {daresults}")

func1()
func2(snack)
func3(x)
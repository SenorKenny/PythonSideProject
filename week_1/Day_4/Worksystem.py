#using for loops to execute tasks
# Start with 4 items and continue
import random
item_number=input("How many different items did you want to buy? ")
cart=[]
Flow=["Inventory","Process","Record"]
stock=[]
desired=[]

for item in range(int(item_number)):
    item_name=input(f"What is item {item+1}? ")
    desired.append(int(input("How many of this item do you want? ")))
    cart.append(item_name) 
    stock.append(random.randint(0,4))

print(stock)
print(cart)

for work in Flow:
    if work == "Inventory":
        for a in range(len(stock)):
            if stock[a]>0:
                continue
            else:
                print(f"Item {cart[a]} is out of stock")
    if work == "Proceess":
        for numb in range(desired):
            bought=[]
            i=desired[numb]
            bought=stock[numb]
            z=stock[numb]
            while i>0 or z>0:
                i -=1
                z -=1
        print(bought)
    if work == "Record":
        for totals in range(len(cart)):
    
         print(f"The number of {cart[totals]}'s bought was {bought[totals]}")




#warm up
#Should be simple. Make a dictionary. 

user1={
    "name":"johhny",
    "fav food":"Shepard's Pie",
    "fav number":16
}
print(user1["name"])
print(user1["fav food"])


#exercise 1 - User's Dictionary

New_User={
    "username":"mylogin",
    "password":"thisispass",
    "age":42
}

for x in New_User:
    print(New_User[x])


#exercise 2 -modification

New_User["password"]="newpass"
New_User.update({"email":"Lol1997@gmail.com"})
print(New_User)
#Exercise 3     Loop through the dictionary. I think i did that?? 
#moved from exercise 2 to 3

print("\n \n The new, updated information for New_user is \n")
for x,y in New_User.items():
    print(f"{x} : {y}")


# Exercise 4: Make 3 dictionaries, store them inside a list

gamer1={
    "Name":"Elliot",
    "age":67,
    "occupation":"retired"
}
gamer2={
    "Name":"LilJohnny",
    "age":25,
    "occupation":"Doctor,Lawyer,Everything"
}
gamer3={
    "Name":"Nutballs",
    "age":33,
    "occupation":"godKnows"
}

ThisListIsBig=[gamer1,gamer2,gamer3]

#Exercise5 loop through each user
print("The name of the gamers playing are: \n")
for gamer in ThisListIsBig:
    for info in gamer:
        if info =="Name":
            print(f"{gamer[info]}\n")

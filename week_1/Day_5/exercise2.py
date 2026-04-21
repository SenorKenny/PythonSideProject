#My attempt at a login checker
import random
server_users=["Penguinxoxo","omgkenny","Xbox4life212","YoutubeSucksNow","TheOddInsect","LeagueIsFun","IfightforEternity","Tits4tat"]
server_passwords=[]
for x in range(len(server_users)):
    server_passwords.append(random.randint(1,6))
Server_database={
    "Username":server_users,
    "Passwords":server_passwords
}

#this will generate a random password for each user every run. The checker will use
# a list of passwords to attempt to login

our_users=["Kenny","omgkenny","DolfinFan21","YoutubeSucksNow","TheOddInsect","LeagueIsFun","IfightforEternity","TiddiesRock"]
our_passwords=[1,2,3]
tries=0
tries_amount=[]
failed_users=[]
#login attempts start now
#need to get list of server_users
#then of the password.
for x in our_users:
    tries=0                     
    while tries <= 3:
        if x in Server_database["Username"]:
            if our_passwords[tries] in Server_database["Passwords"]:
                print(f"User name {x} is a hit")
                tries_amount.append(tries)
                break
            else: 
                tries+=1
        else:
            tries+=1
    else:
        failed_users.append(x)
        print(f" User {x} login information didn't work. Account temporarily locked")

print("The users who failed were \n")
for failures in failed_users:
    print(failures)


print("Attempts user for each user")
for x in range(len(our_users)):
    print(f"{our_users[x]} attempted {tries_amount[x]} logins")




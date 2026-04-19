# Will be checking input usernamee and password vs 
# user name and pass thats in the 'system'

user = "Adriano"
login_email = "elsexylatino@gmail.com"
login_password = "testesto.o"

temp_email = input("Enter your email ")
temp_password = input("Enter your password ")

if login_email != temp_email:
    print("User name or password is incorrect.")
elif login_password != temp_password:
    print("User name or password is incorrect.")
else:
    print("Thank you for verifying,",user,". Welcome")

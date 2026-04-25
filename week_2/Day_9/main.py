
import os
import requests
import json
from dotenv import load_dotenv
load_dotenv()
import requests
#Task 1 , basic calls

serv_response= requests.get("https://jsonplaceholder.typicode.com/todos/1")

print(f"The status code is {serv_response.content}")
print(f"The raw response is {serv_response}")
converted_resp=json.loads(serv_response.text)
print(f"The response was: {converted_resp}")

#task 2, printing specfici parts

print(f"The value of completed is: {converted_resp["completed"]}")
print(f"Thee value of title is {converted_resp["title"]}")


#task 3, new request with queries

new_response=requests.request("GET","https://jsonplaceholder.typicode.com/comments",
                              params={"postId":1,
                                      "id":1}
                              )
#Task4. Make env, make key inside, call , get
apikey=os.getenv("API_key")
print(apikey)

#-------- Minibot project 
print("\n \n \n")

neededresponse=requests.request("GET","https://jsonplaceholder.typicode.com/todos")
neededresponse=neededresponse.json()

for user in neededresponse:

    if user["completed"] == True:
            print(f"Processing task: {user["title"]}")
            print(f"Status {user["completed"]}")
    else:
        continue
requests.request()
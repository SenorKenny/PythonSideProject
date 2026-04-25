import os
import requests
from dotenv import load_dotenv
load_dotenv()


load_dotenv()
def connected(status_code):
    if status_code == 200:
        print ("Success")
    else:
        print ("Error, connection timed out?")

serv_response= requests.get("https://jsonplaceholder.typicode.com/todos/1",timeout=1)


connected(serv_response.status_code)

#Exercise 2, making a try and error for connection and timeout error 
#Exercise 3, multiple attempts
i=0

#Exercise 5, combining it with day 9
#We want to, attempt a connection.
#if no connection, keep retrying 
#if connection, check status code
#if successful, process task, print only completed. 
#if status code is not 200, break
while i<3:
    i+=1
    try:
        success=requests.get("https://jsonplaceholder.typicode.com/todos/",timeout=.0039)
        success.raise_for_status()
        if success:
            print("We did it!")
            print(f"attempts made: {i}")
            break
    except requests.exceptions.HTTPError as e:
            print(f"Error: {e}")
            print(f"attempts made: {i}")
            break
    except (requests.exceptions.Timeout,requests.exceptions.ConnectionError):
        print(f"Attempt {i}:Connection Timeout error ")
    except requests.exceptions.ConnectionError:
        print(f"Attempt {i}:Connection error!")
    except:
        print(f"Attempt {i}:Something else went wrong")
    
else: print(f'attempts made: {i}')



try:
    success
except:
    print("Could not retrieve response")
else:

    success=success.json()

    for user in success:

        if user["completed"] == True:
            print(f"Processing task: {user["title"]}")
             
        else:
            continue

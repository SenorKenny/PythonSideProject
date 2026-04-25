
import os
import requests
from dotenv import load_dotenv
import json
load_dotenv()


load_dotenv()

def fetch_data(url, params_value=None):
    if not params_value:
        params_value={}
    i=0
    while i<3:
        i+=1
        try:
            APIresponse=requests.get(url,params=params_value)
            APIresponse.raise_for_status()
            if APIresponse.status_code != 200:
                print(f'Status code: {APIresponse.status_code}, aborting attempts.')
        
               
                break
            else:
                print("Connection succesful, response recieved")
                print(f"Attempts: {i}")
                return APIresponse.json()
                

        except (requests.exceptions.TimeoutError,requests.exceptions.Timeout):
            print(f"Attempt {i}:Timeout error")
        except requests.exceptions.ConnectionError:
            print(f"Attempt {i}Connection error")
        except requests.exceptions.HTTPError as errors:
            print(f"Attempt {i}: The following error occured: {errors}")
    else:
        print(f"Attempts {i}")
    
    
def process_data(data):
    if data:
        entries=0
        for dictionary_num in data:
            if not dictionary_num["completed"]:
                    entries+=1
                    print(f"Processing task: {dictionary_num['title']}")
                    print(f"completed: {dictionary_num['completed']}")
    else:
        print("Error, no data submitted")
    print(f"Total number of tasks: {entries} ")
response=fetch_data("https://jsonplaceholder.typicode.com/todos")
process_data(response)
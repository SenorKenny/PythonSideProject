
import requests
import random
import time
import config
def  url_requester(url,Timeout_val=None,Param_val=None,header_val=None):
#We want to get response in json and status code. Configurable retry (from env) with sleep built in
    i=0
    retry=config.config["RETRY_ATTEMPTS"]
    while i<retry:
        i+=1
        print(f"Attempt {i}")
        try:
            response=requests.get(url,timeout=Timeout_val,params=Param_val,headers=header_val)
            response.raise_for_status()
            print("Connection Succesful!")
            return response.json(),response.status_code
        except requests.exceptions.ConnectionError:
            print("Connection error. Check URL")
        except requests.exceptions.ConnectTimeout:
            print("Connection timeout. Delay your requests")
        except requests.exceptions.Timeout:
            print("Reader timeout. Server may be busy ")
        except requests.exceptions.HTTPError as error:
            print(f"HTTP error code: {error}")
            return None, response.status_code
        except Exception as othererror:
            print(f"Error is : {othererror}")
        print(f"retrying..")
        sleepfloat=float(random.randint(30,50)/10)
        time.sleep(sleepfloat)
    return None,None
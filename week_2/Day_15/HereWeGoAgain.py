#back to the bot

import os
import requests
import json 
import time
import datetime
from dotenv import load_dotenv
import random


load_dotenv()


def  url_requester(url,Timeout_val=None,Param_val=None,header_val=None):
#We want to get response in json and status code. Configurable retry (from env) with sleep built in
    i=0
    retry=int(os.getenv("REQUEST_RETRY"))
    while i<retry:
        i+=1
        print(f"Attempt {i}")
        try:
            response=requests.get(url,timeout=Timeout_val,params=Param_val,headers=header_val)
            response.raise_for_status()
            return response.json(),response.status_code
        except requests.exceptions.ConnectionError:
            print("Connection error. Check URL")
        except requests.exceptions.ConnectTimeout:
            print("Connection timeout. Delay your requests")
        except requests.exceptions.Timeout:
            print("Reader timeout. Server may be busy ")
        except requests.HTTPError as error:
            print(f"HTTP error code: {error}")
            return
        except Exception as othererror:
            print(f"Error is : {othererror}")
        print(f"retrying..")
        sleepfloat=float(random.randint(30,50)/10)
        time.sleep(sleepfloat)
    return None,None

#Just a simple comprehension buy category. Decision making will be separate function.
def json_parser(json_file):
    try:
        if json_file is None:
            print("Something went wrong with requester.")
            return None
    except Exception as error:
            print(f"Some error unbeknownst to me: {error}")
    
    cat=os.getenv("TARGET_CATEGORY").lower()
    print(cat)
    wanted_products=[x for x in json_file if x.get("category").lower()==cat]
    return wanted_products

#Make Watch+Buy list, compare to a watch/buy list from a json that WE CREATE /already exists
#If duplicates, do not purchase or put again in buy list.
#Need to figure out how to remove
def decision_maker(productlist):
    if productlist is None:
        print("empty input into decisionmaker")
        return None, None
    if not isinstance(productlist,list):
        print("Invalid input. List only")
        return None, None
    maxwatchprice=float(os.getenv("MAX_WATCH"))
    minwatchprice=float(os.getenv("MIN_WATCH"))
    maxbuyprice=float(os.getenv("MAX_BUY"))
    minbuyprice=float(os.getenv("MIN_BUY"))
    print(maxbuyprice)
    print(minbuyprice)
    print(maxwatchprice)
    print(minwatchprice)
    watch_list=[x for x in productlist if maxwatchprice>x.get("price",0)>minwatchprice]
    buy_list=[x for x in productlist if maxbuyprice>x.get("price",0)>minbuyprice]
    # COMPARE.
    # First, confirm there is no json. If not, return our lists. If there i
    try:
        with open("WatchList.json","r") as file:
            compared_watch=json.load(file)
    except FileNotFoundError:
        compared_watch=[]
    except Exception as error:
        print(f"Other error found: {error}")
        return
    if not compared_watch:
        compared_watch=watch_list
    else:

        #watch_list[1-10].get("title") is not in compared_watch. add it to compared_watch
        #same idea with buy list vs bought.
        
        for potential_product in watch_list:
            for current_product in compared_watch:
                if current_product.get("title")!=potential_product.get("title"):
                    addvalue=1
                    continue
                else:
                    addvalue=0
                    break
            if addvalue == 1:
                compared_watch.append(potential_product)







url=os.getenv("API")
converted_request,Status_code=url_requester(url)
productlist=json_parser(converted_request)
x,y=decision_maker(productlist)


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
            return None, response.status_code
        except Exception as othererror:
            print(f"Error is : {othererror}")
        print(f"retrying..")
        sleepfloat=float(random.randint(30,50)/10)
        time.sleep(sleepfloat)
    return None,None

#Just a simple comprehension buy category. Decision making will be separate function.
#
#
#
## Consider making some type of error build up. 
# If main loop keeps failing multiple time, exit the code or
# extend the duration of sleep by an amount for a number of times until the code gives up.

def json_parser(json_file):
    try:
        if json_file is None:
            print("Something went wrong with requester.")
            return None
    except Exception as error:
            print(f"Some error unbeknownst to me: {error}")
    
    cat=os.getenv("TARGET_CATEGORY").lower()
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
    comparison_watch_list=[x for x in productlist if maxwatchprice>x.get("price",0)>minwatchprice]
    buy_list=[x for x in productlist if maxbuyprice>x.get("price",0)>minbuyprice]
    # COMPARE.
    # First, confirm there is no json. If not, return our lists. If there i
    #Watch list is the current loops iteration
    #Goal, make 3 watch lists. first_run, 
    try:
        with open("WatchList.json","r") as file:
            _1stwatch=json.load(file)
    except FileNotFoundError:
        _1stwatch=[]
    except Exception as error:
        print(f"Other error found: {error}")
        return
    if not _1stwatch:
        _1stwatch=comparison_watch_list
    else:

        #comparison_watch_list[1-10].get("title") is not in _1stwatch. add it to _1stwatch
        #same idea with buy list vs bought.
        if #condition for intialization :
            road_map={x.get("title"):x.copy() for x in _1stwatch} ## THIS IS THE ORIGINAL AND PERSISTENT. _1stwatch!
        
        for product in comparison_watch_list:
                name=product.get("title")
                if name not in road_map:
                    _1stwatch.append(product.copy())
                    road_map[name]=product.copy()
                else: 
                    if product.get("price") < road_map.get(name).get("price"):
                        road_map.get(name)["price"]=product.get("price")
        #Now we move on to buying decisions
        for products in _1stwatch:
            name=products.get("title")
            if name in road_map:
                if products.get("price")*.75 > road_map[name].get("price"):
                    buy_list.append(products)
        return buy_list,_1stwatch,road_map
    
    def buyer(buy_list,_1stwatch,road_map):
    
    
    #add checker above for none ig

        for products in buy_list:
            name=products.get("title")
            if random.randint(1,6)<= 3:
                print(f"purchasing {name}")
                road_map.pop(name)
                for originals in _1stwatch:
                    if name in originals.get("title"):
                        del originals

        
                    


            

            ## done, i think
            #next goal, if it is in there, and theres a price change, update price.. could probably add it to
            #original loop. going to try it the set dictionary.

            #test_set_dictionary={x.get("title") for x in _1stwatch}
        







url=os.getenv("API")
converted_request,Status_code=url_requester(url)
productlist=json_parser(converted_request)
x,y=decision_maker(productlist)


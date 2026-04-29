#back to the bot

import os
import requests
import json 
import time
import datetime
from dotenv import load_dotenv
import random
import copy


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
def decision_maker(productlist,initial_1st,road_map,first_run):
    flag_basewatch=False
    flag_liveloop=False
    _1stwatch=initial_1st
    if productlist is None:
        print("empty input into decisionmaker")
        return None, None,None,None,None
    if not isinstance(productlist,list):
        print("Invalid input. List only")
        return None, None,None,None,None
    maxwatchprice=float(os.getenv("MAX_WATCH"))
    minwatchprice=float(os.getenv("MIN_WATCH"))
    maxbuyprice=float(os.getenv("MAX_BUY"))
    minbuyprice=float(os.getenv("MIN_BUY"))
    comparison_watch_list=[x for x in productlist if maxwatchprice>x.get("price",0)>minwatchprice]
    buy_list=[x for x in productlist if maxbuyprice>x.get("price",0)>minbuyprice]
    # COMPARE.
    # First, confirm there is no json. If not, return our lists. If there i
    #Watch list is the current loops iteration
    #Goal, make 3 watch lists. first_run,
    if first_run:
        try:
            with open("WatchList.json") as file:
                _1stwatch=json.load(file)
        except FileNotFoundError:
            _1stwatch=[]
        except json.JSONDecodeError as error:
            _1stwatch=[]
            print(f"Other error found: {error}")
            return None,None,None,None,None
        if not _1stwatch:
            _1stwatch=comparison_watch_list

        #comparison_watch_list[1-10].get("title") is not in _1stwatch. add it to _1stwatch
        #same idea with buy list vs bought.
    if first_run:
            try:
                with open("Live_watchlist.json") as file:
                    road_map=json.load(file)
            except:
                road_map={x.get("title"):x.copy() for x in _1stwatch} ## THIS IS THE ORIGINAL AND PERSISTENT. _1stwatch!
        
    for product in comparison_watch_list:
                name=product.get("title")
                if name not in road_map:
                    _1stwatch.append(product.copy())
                    road_map[name]=product.copy()
                    flag_basewatch=True
                    flag_liveloop=True
                else: 
                    if product.get("price") < road_map.get(name).get("price"):
                        road_map.get(name)["price"]=product.get("price")
                        flag_liveloop=True
        #Now we move on to buying decisions
    for products in _1stwatch:
            name=products.get("title")
            if name in road_map:
                if products.get("price")*.75 > road_map[name].get("price"): #If the updated price is less than
                    buy_list.append(products)  #75% of the original price upon start up, then we buy.
                    
    return buy_list,_1stwatch,road_map,flag_basewatch,flag_liveloop
    
    
    
def buyer(buy_list,_1stwatch,road_map):
    flag_basewatch=False
    flag_liveloop=False
    flag_purchase=False
    #add checker above for none ig
    purchased=[]
    for products in buy_list:
            name=products.get("title")
            if random.randint(1,6)<= 3:
                print(f"purchasing {name}")
                purchased.append(products)
                flag_purchase=True
                if name in road_map: 
                    road_map.pop(name,None) # This will pop the one from road_map. Then remove from first watch without altering object. Add to purchased
                    _1stwatch[:]=[x for x in _1stwatch if x.get("title") != name]
                flag_basewatch=True
                flag_liveloop=True
            else:
                print(f"failed to purchase {name}")
    buy_list[:]=[x for x in buy_list if x not in purchased]
    return purchased,flag_purchase,flag_basewatch,flag_liveloop
    

        #improvements. the filtered from decision maker into parser, put buying and decision maker in one function
def file_saver(_1stwatch,road_map,purchased,dictionary):
        
        if dictionary.get("flag_liveloop"):
            with open("Live_watchlist.json","w") as file:
                json.dump(road_map,file, indent=4)
        
        if dictionary.get("flag_basewatch"):
            with open("Base_watchlist.json","w") as file:
                json.dump(_1stwatch,file,indent=4)
        
        if dictionary.get("flag_purchase"): 
            with open("Purchases.json","w") as file:
                json.dump(purchased,file,indent=4)
        return                    
def logger(dictionary,purchased,buy_list):
        timenow=datetime.datetime.now()
        fails=len(buy_list)-len(purchased)

        with open("Logger_Summary.txt","a") as file:
            print(timenow,file=file)
            print(f"{len(purchased)} items purchased, {fails} failed, ", file=file)
            if dictionary.get("flag_basewatch") or dictionary.get("flag_liveloop"):
                print("Watchlist changed",file=file)
def terminaloutput(start_time,purchased,watchlist,i):
    end_time=datetime.datetime.now()
    print("="*100)
    print(f"Script started at {start_time}")
    print(f"Products purchased: {len(purchased)}")
    print(f"Number of products in watchlist:{watchlist}")
    print(f"Number of loops: {i}")
    print(f"End time: {end_time}")
    print("="*100)
    

i=0
first_run=1
start_time=datetime.datetime.now()
_1stwatch=None
road_map=None
try:
    while True:
        
        i=i+1
        print(f"Loop {i}")
        
        url=os.getenv("API")
        converted_request,Status_code=url_requester(url)
        productlist=json_parser(converted_request)
        buylist,_1stwatch,road_map,flag_basewatch,flag_liveloop=decision_maker(productlist,_1stwatch,road_map,first_run)
        purchases,flag_purchase,flag_basewatch2,flag_liveloop2=buyer(buylist,_1stwatch,road_map)

        if flag_basewatch or flag_basewatch2:
            flag_basewatch=True
        if flag_liveloop or flag_liveloop2:
            flag_liveloop=True
        booleanDictionary={"flag_basewatch":flag_basewatch,
                        "flag_liveloop":flag_liveloop,
                        "flag_purchase":flag_purchase
        }
        file_saver(_1stwatch,road_map,purchases,booleanDictionary)
        logger(booleanDictionary,purchases,buylist)
        if first_run == 1:
            first_run=0
        time.sleep(10)
except KeyboardInterrupt:
    terminaloutput(start_time,purchases,_1stwatch,i)
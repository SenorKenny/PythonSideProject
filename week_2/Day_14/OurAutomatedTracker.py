
#My Attempt at a fulled automated task:A product purchaser 
#It will attempt to keep looping the script until certain keys are pressed
# It will Attempt to do the following tasks
#Send a request--> Translate the response--> Sparse the info--> Make a decision-->Log actions--> 
# ---> Loop everything. Print a terminal command upon completion 

import os
from dotenv import load_dotenv
import datetime
import json
import requests
import random
import time

load_dotenv()




target_store=os.getenv("API")
##Make sure to add values to return 
##Requests data from server with given parameters. Retries and prints error codes if something is wrong.
def my_requester(theurl,timeoutval=2,ourheader=None,ourparams=None):
    try:
        maxretries=int(os.getenv("MAX_RETRIES"))
    except Exception as error:
        maxretries=3
        print(f"Wrong path from env: error {error}")
    i=0
    while i<maxretries:
        i+=1
        print(f"Attempt {i}:")
        try:
            response=requests.get(theurl,timeout=timeoutval,params=ourparams,headers=ourheader)
            response.raise_for_status()
            return response
        except requests.exceptions.Timeout:
            print("Timeout error")
        except requests.exceptions.ConnectionError:
            print("Connection error")
        except requests.exceptions.HTTPError as error:
            print(f"Status code {response.status_code}: {error}")
            return None
        except requests.exceptions.ConnectTimeout:
            print("Connection Timeout error")
        except Exception as errors:
            print(f"Unknown error, error output:{error}")
        print("\n Retrying...\n")
        time.sleep(i*2)
    return None



def json_sparser(data):
    try:
        ThisList=data.json()
    except:
        print("Error: no data")
        return
    # going to do a comprehension as tuple that gives products, category, and price for a given category
    try:
        itemprice=float(os.getenv("MAX_PRICE"))
        cat=os.getenv("TARGET_CATEGORY").lower()
        
    
    except Exception as sparser_error:
        print(f"DEBUG error in os.getenv: Errror {sparser_error}")
        return None, None
    try:
        
        new_list=[(x.get("title"),x.get("price"),x.get("category")) for x in ThisList 
                if x.get("category").lower() == cat.lower() and x.get("price",0)<itemprice]
        func_code=1
        return new_list,func_code
    except Exception as sparser_error:
        print(f"DEBUG: Errror with list comphrension: {sparser_error}")
        return None, None
    

# if price is in a certain threshold , buy. If in another, add to a watch list?
def my_decision_maker(data,func_code):

    if data is None and func_code==1:
        print("Nothing products could be bought or watched")
        return None,None,None
    if data is None:
        print("Debug in deecision maker, no input detected")
        return None,None,None
    watch_list=[]
    buy_list=[]
    try:
        maxwatch=float(os.getenv("MAX_WATCH_PRICE"))
        minwatch=float(os.getenv("MIN_WATCH_PRICE"))
        maxbuy=float(os.getenv("MAX_BUY_PRICE"))
        minbuy=float(os.getenv("MIN_BUY_PRICE"))
    except Exception as decision_error:
        print(f"Error in os.path logic for decision maker: {decision_error}")

    for x in data:
        if x[1] < maxwatch and x[1]>minwatch:
            watch_list.append((x[0],x[1]),"watching") #puts item namee and Category
        if  x[1] >minbuy and x[1] <maxbuy:
            buy_list.append(x[0],x[1])
        else:
            continue
    purchased=[]
    not_purchased=[]
    for x in buy_list:
        if random.randint(1,6)<6:
           # (f" Item {x[1]} was purchased"). the idea.. maybe save it to the logger at end?
            
            purchased.append(*x,"Success")
        else:
            not_purchased.append(*x,"Failed")
    return watch_list, purchased, not_purchased

def my_logger(sparsed_data,bought,failed,code):
    current_time=datetime.datetime.now()
    if isinstance(code,int):
        if code == 200:
            event="Success!"
        else:
            event="Failure!"
    else:
        print("No input for status code")
        return
    
    if isinstance(sparsed_data,list) and isinstance(bought,list) and isinstance(failed,list):
        numitems=len(sparsed_data)
        numpurchase=len(bought)
        numfailed=len(failed)
    try:
        with open("Log_Summary.txt","a") as zefile:
            print(f"{current_time}: {event}",file=zefile)
            if "Success!" in event:
                print(f"{numitems} items found , {numpurchase} items bought, {numfailed} purchases failed\n",file=zefile)
            return
    except Exception as error:
        print(f"Something went wrong in file creating or gathering input: {error}")
    return


def my_jason_saver(data):
    if data:
        current_time=datetime.datetime.now()
        This_new_line=(*data,current_time)

        try:
            with open("Products.json","r") as ourjson:
                json_list=json.load(ourjson)
        except json.JSONDecodeError:
            json_list=[]
        except Exception as e:
            print(f"Error found: {e}")
            return
        
        json_list.append(This_new_line)
        with open("Products.json","w") as NewLines:
            json.dump(json_list)
        return
    return






def terminal_output(starttime,endtime,items,watch,bought,failed,loops):
    print("\n"+"="*100)
    print("Summary of todays actions \n")
    print(f"Start time: {starttime}\n")
    print(f"items found: {items}\n")
    print(f"items on watch list:{watch}\n")
    print(f"items purchased:{bought}\n")
    print(f"purchases failed:{failed}\n")
    print(f"Number of times this script was executed: {loops} \n")
    print(f"Ending at {endtime}\n")
    print("="*100)
    return

execution=0
OurStart=datetime.datetime.now()
try:
    while True:
        execution+=1
        print(f"Attemping Loop {execution}")
        target_store=os.getenv("API")
        Headerval= None #for now set to none
        # use Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36
        #later to test
        Newjson=my_requester(target_store)
        filtered_list,zecode=json_sparser(Newjson)
        watch,purchased,notpurchased=my_decision_maker(filtered_list,zecode)
        my_logger(filtered_list,purchased,notpurchased,Newjson.status_code)
        my_jason_saver(filtered_list)
        
        time.sleep(180)
except KeyboardInterrupt:
    the_end=datetime.datetime.now()
try:
    terminal_output(OurStart,the_end,len(filtered_list),len(watch),len(purchased),len(notpurchased),execution)
except:
    print("You couldn't even get past first execution, scrubnuts")

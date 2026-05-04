#back to the bot

import os
import requests
import json 
import time
import datetime
from dotenv import load_dotenv
import random
import statistics


load_dotenv()

class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return super().default(obj)

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


def json_parser(json_file,schema,purchased):
    
    boolean_dictionary={"item_entry":False,
                        "watch_update":False}
    try:
        if json_file is None:
            print("Something went wrong with requester.")
            return None,boolean_dictionary
    except Exception as error:
            print(f"Some error unbeknownst to me: {error}")
            return None,boolean_dictionary
    
    too_high=float(os.getenv("MAX_WATCH"))
    for x in json_file:
        
        price=abs(round(float(x.get("price",0)),2))
        if price>too_high:
             continue
        name=x.get("title","N/A").lower().strip()
        if name in purchased:
             continue
        if name in schema:
            if "watching" in schema[name]["status"]:
                 if price != schema[name]["price"]:
                      schema[name]["temp_price"]=price
                      schema[name]["price_history"].add(price)
                      first_time=str(datetime.datetime.now())
                      schema[name]["last_time"].append(first_time)
                      boolean_dictionary["watch_update"]=True
            else:
                 continue
        else:
            boolean_dictionary["item_entry"]=True
            category=x.get("category","").lower().strip()
            if isinstance(category,(tuple,list,)):
                category=category[0].lower().strip()
            else:
                category=category.lower().strip()
        
            if "electronics" in category:
                priority = 1
            elif "kitchen" in category:
                priority = 3
            elif "shoes" in category:
                priority = 2
            else:
                continue
            inventory=True
            price_history=price
            first_time=str(datetime.datetime.now())
            last_time=[first_time]
            status="N/A"
            bought=0
            schemadetails={
                    "price":price,
                    "inventory":inventory,
                    "priority":priority,
                    "category":category,
                    "price_history":{price_history},
                    "status":status,
                    "bought":bought,
                    "first_seen":first_time,
                    "last_time":last_time
                    }
            schema[name]=schemadetails
    return boolean_dictionary

def decision_maker(schema,boolean_dictionary):
    boolean_dictionary["buying"]=False
    if schema is None:
        print("empty input into decisionmaker")
        return None
    if not isinstance(schema,dict):
        print("Invalid input. Dictionary only")
        return None
    max_watchprice=float(os.getenv("MAX_WATCH"))
    max_buyprice=float(os.getenv("MAX_BUY"))
    min_watchprice=float(os.getenv("MIN_WATCH"))
    min_buyprice=float(os.getenv("MIN_BUY"))
    currentignore={}
    if boolean_dictionary["watch_update"]: #Should see if temp_price and watch_update are true
        for values in schema.values():   #will pop temp_price at end
            if "temp_price" in values:
                buyprice=0.75*statistics.median(values["price_history"])
                if buyprice>values["temp_price"]:
                    values["status"]="buying"
                    boolean_dictionary["buying"]=True
                    values.popitem("temp_price")
                else:
                    values.popitem("temp_price")
    if boolean_dictionary["item_entry"]: 
        for name in schema: #this updates for items not yet listed
            if schema[name]["status"] == "N/A":
                productprice=schema[name]["price"]  
                if min_watchprice<=productprice<=max_watchprice:
                    schema[name]["status"]="watching"
                    continue
                elif min_buyprice<=productprice<=max_buyprice:
                    schema[name]["status"]="buying"
                    boolean_dictionary["buying"]=True
                    continue
        
    return 
    
def buyer(schema,boolean_dictionary,purchased):
    boolean_dictionary["purchased"]=False
    fails=0
    if not boolean_dictionary["buying"]:
        return schema,fails
    
    for name in schema:
        if "buying" in schema[name]["status"]:    
            if random.random()<=.5:
                print(f"purchasing {name}")
                purchased.add(name)
                flag_purchase=True
                schema[name]["status"]="purchased"
                purchased.add(name)
                boolean_dictionary["purchased"]=True
            else:
                print(f"failed to purchase {name}")
                schema[name]["status"]="failed"
                fails+=1
    schema={x:y for x,y in schema.items() if y["status"]!="purchased"}
    return schema,fails
        #improvements. the filtered from decision maker into parser, put buying and decision maker in one function

def file_saver(schema,purchased,boolean_dictionary):
        
        if boolean_dictionary["item_entry"] or boolean_dictionary["watch_update"]:
            with open("products.json","w") as file:
                json.dump(schema, file, indent=4, cls=SetEncoder)

        if boolean_dictionary["purchased"]:
            with open("purchases.json","w") as file:
                json.dump(purchased,file,indent=4,cls=SetEncoder)
        return   

def logger(purchased,fails):
    timenow=datetime.datetime.now()
    
    with open("Logger_Summary.txt","a") as file:
        print(timenow,file=file)
        print(f"{len(purchased)} items purchased, {fails} failed, ", file=file)

def terminaloutput(start_time,purchased,schema,i):
    end_time=datetime.datetime.now()
    print("="*100)
    print(f"Script started at {start_time}")
    print(f"Products purchased: {len(purchased)}")
    print(f"Number of products we're watching:{len(schema)}")
    print(f"Number of loops: {i}")
    print(f"End time: {end_time}")
    print("="*100)

i=0
start_time=datetime.datetime.now()
try:
            with open("products.json","r") as file:
                schema=json.load(file)
                for item in schema.values():
                    item["price_history"] = set(item["price_history"])
except FileNotFoundError:
                schema={}
except json.JSONDecodeError:
                schema={}
except Exception as e:
            print(f"Error here: {e}")
            schema={}
try:
            with open("purchases.json","r") as file:
                purchased=json.load(file)
                purchased=set(purchased)
except FileNotFoundError:
                purchased=set()
except json.JSONDecodeError:
                purchased=set()
except Exception as e:
            print(f"Error here: {e}")
            purchased=set()
try:
    while True:
        
        i=i+1
        print(f"Loop {i}")
        
        url=os.getenv("API")
        converted_request,Status_code=url_requester(url)
        boolean_dictionary=json_parser(converted_request,schema,purchased)
        decision_maker(schema,boolean_dictionary)
        schema,fails=buyer(schema,boolean_dictionary,purchased)
        file_saver(schema,purchased,boolean_dictionary)
        logger(purchased,fails)
        time.sleep(10)
except KeyboardInterrupt:
    terminaloutput(start_time,purchased,schema,i)
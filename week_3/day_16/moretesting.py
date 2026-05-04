
import datetime
import time
import os
from dotenv import load_dotenv
import statistics
import random
load_dotenv()
import json

class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return super().default(obj)


def json_parser(json_file,schema,purchased):
    
    item_entry=False
    watch_update=False
    boolean_dictionary={"item_entry":item_entry,
                        "watch_update":watch_update}
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
                      schema[name][last_time].append(first_time)
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
                    "last_seen":last_time
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
                    values["statues"]="buying"
                    boolean_dictionary["buying"]=True
                    values.popitem()
                else:
                    values.pop()
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
def logger(boolean_dictionary,purchased,fails):
    timenow=datetime.datetime.now()
    if boolean_dictionary["item_entry"] or boolean_dictionary["watch_update"]:
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
    
productlist=[
    # Normal cases — happy path
    {"title": "Sony WH-1000XM5 Headphones", "price": 349.99, "category": "electronics"},
    {"title": "Nike Air Max 90", "price": 129.99, "category": "shoes"},
    {"title": "Instant Pot Duo 7-in-1", "price": 79.95, "category": "kitchen"},
    {"title": "Levi's 501 Original Jeans", "price": 59.50, "category": "clothing"},
    {"title": "Logitech MX Master 3S", "price": 99.99, "category": "electronics"},
    
    # Same products at different prices — for testing updates
    {"title": "Sony WH-1000XM5 Headphones", "price": 329.99, "category": "electronics"},
    {"title": "Nike Air Max 90", "price": 129.99, "category": "shoes"},  # unchanged price
    {"title": "Instant Pot Duo 7-in-1", "price": 64.99, "category": "kitchen"},  # real drop
    
    # Edge case: missing price field
    {"title": "Apple AirPods Pro 2", "category": "electronics"},
    
    # Edge case: price as string instead of float
    {"title": "Kindle Paperwhite", "price": "139.99", "category": "electronics"},
    
    # Edge case: zero price (probably an error from the site)
    {"title": "Roku Streaming Stick", "price": 0, "category": "electronics"},
    
    # Edge case: negative price (definitely an error)
    {"title": "Bose QuietComfort Earbuds", "price": -49.99, "category": "electronics"},
    
    # Edge case: missing title
    {"price": 199.99, "category": "electronics"},
    
    # Edge case: empty title
    {"title": "", "price": 24.99, "category": "books"},
    
    # Edge case: title with weird whitespace/casing — is "iPad Air" same as " ipad air "?
    {"title": "  iPad Air  ", "price": 599.00, "category": "electronics"},
    {"title": "ipad air", "price": 599.00, "category": "electronics"},
    
    # Edge case: missing category
    {"title": "Stanley Quencher 40oz", "price": 44.99},
    
    # Edge case: category as list (your schema expects list anyway)

    
    # Edge case: huge price (possible parsing error or genuine luxury item?)
    {"title": "Rolex Submariner", "price": 14500.00, "category": "watches"},
    
    # Edge case: extra fields you didn't ask for
    {"title": "Yeti Rambler 20oz", "price": 35.00, "category": "kitchen", "color": "blue", "weight": "1.2lbs"},
    
    # Normal items to round it out
    {"title": "Anker PowerCore 10000", "price": 25.99, "category": "electronics"},
    {"title": "Hydro Flask 32oz", "price": 44.95, "category": "kitchen"},
    {"title": "Allbirds Wool Runners", "price": 110.00, "category": "shoes"},
    {"title": "Dyson V15 Detect", "price": 749.99, "category": "appliances"},
    {"title": "Patagonia Better Sweater", "price": 139.00, "category": "clothing"},
    
    # More repeats with price changes for testing history accumulation
    {"title": "Sony WH-1000XM5 Headphones", "price": 319.99, "category": "electronics"},  # 3rd sighting, dropping
    {"title": "Logitech MX Master 3S", "price": 89.99, "category": "electronics"},  # 2nd sighting, drop
    {"title": "Logitech MX Master 3S", "price": 89.99, "category": "electronics"},  # 3rd sighting, unchanged
    {"title": "Instant Pot Duo 7-in-1", "price": 89.99, "category": "kitchen"},  # 3rd sighting, price went UP
    
    # Edge case: identical product appearing twice in same fetch (rare but happens)
    {"title": "Echo Dot 5th Gen", "price": 49.99, "category": "electronics"},
    {"title": "Echo Dot 5th Gen", "price": 49.99, "category": "electronics"},
]


schema={}
i=1
purchased=set()
moment=datetime.datetime.now()
boolean_dictionary=json_parser(productlist,schema,purchased)
decision_maker(schema,boolean_dictionary)
schema,fails=buyer(schema,boolean_dictionary,purchased)
file_saver(schema,purchased,boolean_dictionary)
logger(boolean_dictionary,purchased,fails)
terminaloutput(moment,purchased,schema,i)

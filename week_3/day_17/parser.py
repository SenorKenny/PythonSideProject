
import datetime
import config
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
    
    too_high=config.config["MAX_WATCHPRICE"]
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
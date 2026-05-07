
import statistics
import config
import random
import logging
logger = logging.getLogger(__name__)

def status_updater(schema,boolean_dictionary):
    boolean_dictionary["buying"]=False
    if schema is None:
        logging.error("No input for SCHEMA")
        return None
    if not isinstance(schema,dict):
        logging.error ("Schema is not in dictionary mode")
        return None
    max_watchprice=config.config["MAX_WATCHPRICE"]
    max_buyprice=config.config["MAX_BUYPRICE"]
    min_watchprice=config.config["MIN_WATCHPRICE"]
    min_buyprice=config.config["MIN_BUYPRICE"]
    currentignore={}
    if boolean_dictionary["watch_update"]: #Should see if temp_price and watch_update are true
        for values in schema.values():   #will pop temp_price at end
            if "temp_price" in values:
                buyprice=0.75*statistics.median(values["price_history"])
                if buyprice>values["temp_price"]:
                    values["status"]="buying"
                    boolean_dictionary["buying"]=True
                    values.pop("temp_price",None)
                    logger.info("Changing info status to buy")
                else:
                    values.pop("temp_price",None)
                    logger.info("Popping temp_price from schema")
    if boolean_dictionary["item_entry"]: 
        for name in schema: #this updates for items not yet listed
            if schema[name]["status"] == "N/A":
                productprice=schema[name]["price"]  
                if min_watchprice<=productprice<=max_watchprice:
                    schema[name]["status"]="watching"
                    logger.info("Product in schema changed from N/A to status")
                    continue
                elif min_buyprice<=productprice<=max_buyprice:
                    schema[name]["status"]="buying"
                    boolean_dictionary["buying"]=True
                    logger.info("Product in Schema changed to BUYING")
                    continue
        
    return

import random

def buyer(schema,boolean_dictionary,purchased):
    boolean_dictionary["purchased"]=False
    fails=0
    if not boolean_dictionary["buying"]:
        logger.info("No products being purchased")
        return schema,fails
    
    for name in schema:
        if "buying" in schema[name]["status"]:    
            if random.random()<=.5:
                logger.info(f"purchasing {name}")
                purchased.add(name)
                flag_purchase=True
                schema[name]["status"]="purchased"
                purchased.add(name)
                boolean_dictionary["purchased"]=True
            else:
                print(f"failed to purchase {name}")
                schema[name]["status"]="failed"
                fails+=1
                logger.warning(f"failed to purchase {name}")
    schema={x:y for x,y in schema.items() if y["status"]!="purchased"}
    logger.debug("Made changes to schema")
    return schema,fails
        #improvements. the filtered from decision maker into parser, put buying and decision maker in one function


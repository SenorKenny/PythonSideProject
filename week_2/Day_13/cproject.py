import os
import requests
from dotenv import load_dotenv
from datetime import datetime
import json
load_dotenv()


def fetcher(url,timeout_time=2,paramvals=None):
    num_of_attempts=0
    this_int=os.getenv("MAX_RETRIES")
    while num_of_attempts < int(this_int):
        num_of_attempts+=1
        try:
            response=requests.get(url, timeout=timeout_time,params=paramvals)
            response.raise_for_status()
            
            return response.json(), num_of_attempts,response.status_code
        except requests.exceptions.ConnectTimeout:
            print("Connection Timeout Error.")
        except requests.exceptions.ConnectionError:
            print("Connection Error")
        except requests.exceptions.HTTPError as e:
            print(f"Error {e}")
            return [],num_of_attempts,response.status_code
        except requests.exceptions.Timeout:
            print("Timeout Error")
        except Exception as error:
            print(f"Not sure what error is, code:{error}")
        print("retrying..")
    else:
        return [],num_of_attempts,0
    
def parsehere(data):
    if not data:
        print("DEBUG: Data is empty")
        return [], 0
    
    # Check if variables actually exist
    raw_price = os.getenv("MAX_PRICE")
    cat = os.getenv("TARGET_CATEGORY").lower()
    
    print(f"DEBUG: Filtering for {cat} below ${raw_price}")

    try:
        price = float(raw_price)
        newlist = [
            {"Product_name": x.get("title"), "Price": x.get("price", 0), "Category": x.get("category")} 
            for x in data 
            if x.get("price", 0) < price and x.get("category").lower() == cat
        ]
        
        print(f"DEBUG: Matches found: {len(newlist)}")
        return newlist, len(newlist)

    except Exception as e:
        print(f"DEBUG: Crash during parsing: {e}")
        return [], 0

def savejson(info):
    if not info:
        print("Something is wrong with info argument")
        return
    time=datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    final_product={
        "Timestamp":time,
        "Products":info
    }
    filename="products.json"
    if os.path.exists(filename) and os.path.getsize(filename):
        with open(filename,"r") as zefile:
            try:
                snapshot=json.load(zefile)
            except json.JSONDecodeError:
                snapshot=[]
    else:
        snapshot=[]
    snapshot.append(final_product)
    with open(filename,"w") as zefile:
        json.dump(snapshot,zefile, indent=4)

def logger(numberofproducts,status_code,):
    #If file doesn't exist, makes file. If does, append"
    if numberofproducts is None or status_code is None:
        return
    our_file_name="The_Logs.txt"
    time=datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    if status_code == 200:
        SuccFail="SUCCESS"
    else:
        SuccFail="FAILURE"
    statement=f"{time}: {SuccFail} found {numberofproducts} number of products that matched our search"
    with open(our_file_name,"a") as zefile:
        print(statement,file=zefile)
    





our_json,attemptnum,our_statuscode=fetcher("https://fakestoreapi.com/products")
filtered_products,num_of_prod=parsehere(our_json)
savejson(filtered_products)
logger(num_of_prod,our_statuscode)


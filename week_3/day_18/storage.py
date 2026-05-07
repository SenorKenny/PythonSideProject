
import json
import datetime
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)

class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return super().default(obj)

def load_files():
    try:
                with open("products.json","r") as file:
                    schema=json.load(file)
                    for item in schema.values():
                        item["price_history"] = set(item["price_history"])
    except FileNotFoundError:
                    logging.exception("purchases.json not found")
                    schema={}
    except json.JSONDecodeError:
                    logging.exception("products.json file corrupted")
                    schema={}
    except Exception as e:
                logging.exception(f"products.json file error {e}")
                
                schema={}
    try:
                with open("purchases.json","r") as file:
                    purchased=json.load(file)
                    purchased=set(purchased)
    except FileNotFoundError:
                    logging.exception("purchases.json not found")
                    purchased=set()
    except json.JSONDecodeError:
                    logging.exception("purchases.json file corrupted")
                    purchased=set()
    except Exception as e:
                logging.exception(f"Error here: {e}")
                purchased=set()
    return schema,purchased

def data_logger(purchased,fails):
    timenow=datetime.datetime.now()
    
    with open("Logger_Summary.txt","a") as file:
        print(timenow,file=file)
        print(f"{len(purchased)} items purchased, {fails} failed, ", file=file) 
        logger.info("adding info to Logger_summary")

def file_saver(schema,purchased,boolean_dictionary):
    
        if boolean_dictionary["item_entry"] or boolean_dictionary["watch_update"]:
            logger.info("Updating products.json")
            with open("products.json","w") as file:
                json.dump(schema, file, indent=4, cls=SetEncoder)  
        if boolean_dictionary["purchased"]:
            logger.info("Updating purchases.json")
            with open("purchases.json","w") as file:
                json.dump(purchased,file,indent=4,cls=SetEncoder)
                
        return   

import json
import datetime

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
    return schema,purchased

def logger(purchased,fails):
    timenow=datetime.datetime.now()
    
    with open("Logger_Summary.txt","a") as file:
        print(timenow,file=file)
        print(f"{len(purchased)} items purchased, {fails} failed, ", file=file) 


def file_saver(schema,purchased,boolean_dictionary):
    
        if boolean_dictionary["item_entry"] or boolean_dictionary["watch_update"]:
            with open("products.json","w") as file:
                json.dump(schema, file, indent=4, cls=SetEncoder)

        if boolean_dictionary["purchased"]:
            with open("purchases.json","w") as file:
                json.dump(purchased,file,indent=4,cls=SetEncoder)
        return   

import random

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


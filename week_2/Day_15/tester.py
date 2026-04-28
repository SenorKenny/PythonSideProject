

list_1=  [{
    "title":"cats",
    "name":"sasha",
    "color":"grey",
    "weight":10
},{
    "title":"cats",
    "name":"tab",
    "color":"orange",
    "weight":15
},{
    "title":"cats",
    "name":"coco",
    "color":"red",
    "weight":6
}]

list_2=[{
    "title":"cats",
    "name":"sasha",
    "color":"grey",
    "weight":13
},{
    "title":"cats",
    "name":"Kiwi",
    "color":"grey",
    "weight":9
}]
####

##====================================================== trying set dicitionary

set_list={old.get("name") for old in list_1}
print(set_list)

for names in list_2:
    if names.get("name") not in set_list:
        list_1.append(names)
    else:
        addition=[names.keys]

print(addition)
        



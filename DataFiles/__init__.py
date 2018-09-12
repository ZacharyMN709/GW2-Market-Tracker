import os

direc = "DataFiles/"
files = ["StaticData", "DynamicData", "DynamicInventory",
         "ItemsMasterList", "RecipesMasterList",
         "MaterialsMasterList", "UncraftableMasterList"]

def WriteStaticLists(API, baseURL, timeout, directory, outputperline, merchant_list, d=direc):
    print("Writing data to StaticData.py...")
    with open(d+'StaticData.py', 'w') as f:
        f.write("## API Status: https://status.gw2efficiency.com/")
        f.write("API = " + str(API) + '\n')
        f.write("baseURL = " + str(baseURL) + '\n')
        f.write("timeout = " + str(timeout) + '\n')
        f.write("directory = " + str(directory) + '\n')
        f.write("outputperline = " + str(outputperline) + '\n')
        f.write("merchant = {" + ", \n\t".join(merchant_list) + "\n}\n\n")

def WriteDynamicLists(items, recipes, d=direc):
    items_list = [(str(i) + ": " + str(items.get(i))) for i in items]
    recipes_list = [(str(r) + ": " + str(recipes.get(r))) for r in recipes]
    items_list.sort(reverse=True)
    recipes_list.sort(reverse=True)
    print("Writing data to DynamicData.py...")
    with open(d+'DynamicData.py', 'w') as f:
        f.write("items = {" + ", \n\t ".join(items_list) + "\n\t}\n\n")
        f.write("recipes = {" + ", \n\t   ".join(recipes_list) + "\n\t  }\n\n")

def WriteInventoryList(inventory, last_buy, last_sell, d=direc):
    inventory_list = [(str(i) + ": " + str(inventory.get(i))) for i in inventory]
    inventory_list.sort(reverse=True)
    print("Writing data to DynamicInventory.py...")
    with open(d+'DynamicInventory.py', 'w') as f:
        f.write("inventory = {" + ", \n\t     ".join(inventory_list) + "\n\t    }\n\n")
        f.write("last_buy = '" + str(last_buy) + "'\n")
        f.write("last_sell = '" + str(last_sell) + "'\n")

def WriteMasterItems(items, d=direc):
    items_list = []
    for x in items:
        key = " "*(7-len(str(x))) + str(x)
        val = str(items[x]).replace(r'"', r'\"')
        items_list.append(key + ': "' + val + '"')
    import codecs
    with codecs.open(d+'ItemsMasterList.py', 'w', "utf-8") as a:
        a.write("master_item_list = {\n" + ", \n".join(items_list) + "\n}")
        
def WriteMasterRecipes(recipes, d=direc):
    recipes_list = []
    for x in recipes:
        key = " "*(7-len(str(x))) + str(x)
        recipes_list.append(key + ': ' + str(recipes[x]))
    with open(d+'RecipesMasterList.py', 'w') as b:
        b.write("master_recipe_list = {\n" + ", \n".join(recipes_list) + "}")

def WriteMasterMaterials(materials, d=direc):
    materials = sorted(list(materials))
    crafting_materials = [str(x) for x in materials]
    with open(d+'MaterialsMasterList.py', 'w') as c:
        c.write("crafting_materials = set([\n" + ", \n".join(crafting_materials) + "])")

def WriteMasterUncraftables(uncraftables, d=direc):
    uncraftables = sorted(list(uncraftables))
    uncraftable_list = [str(x) for x in uncraftables]
    with open(d+'UncraftableMasterList.py', 'w') as f:
        f.write("uncraftables = set([\n" + ", \n".join(uncraftable_list) + "])")


def fileGen(file, d=direc):
    fix = None
    if(file in files):
        fix = file
        if(file == "StaticData"):
            WriteStaticLists(None, "https://api.guildwars2.com/v2/", 10, "/TextFiles", 4, "", d=d)
        elif(file == "DynamicData"):
            WriteDynamicLists({}, {}, d=d)
        elif(file == "DynamicInventory"):
            WriteInventoryList({}, None, None, d=d)
        elif(file == "ItemsMasterList"):
            WriteMasterItems([])
        elif(file == "RecipesMasterList"):
            WriteMasterRecipes([""])
        elif(file == "MaterialsMasterList"):
            WriteMasterMaterials([""])
        elif(file == "UncraftableMasterList"):
            WriteMasterUncraftables([""])
    return fix

def fileFix(fixes, d=direc):
    import Seeder as S
    for file in fixes:
        if(file in files):
            fix = file
            if(file == "StaticData"):
                S.SetStaticLists(True)
            elif(file == "DynamicData"):
                ids = None
                while True:
                    ids = input("Enter an item ID:")
                    if(type(ids) == int): break
                S.SetDynamicLists(ids)
            elif(file == "DynamicInventory"):
                S.SetInventoryList()
            elif(file == "ItemsMasterList"):
                S.SetMasterItems()
            elif(file == "RecipesMasterList"):
                if("UncraftableMasterList" in fixes): fixes.remove("UncraftableMasterList")
                S.SetMasterRecipes()
            elif(file == "UncraftableMasterList"):
                if("RecipesMasterList" in fixes): fixes.remove("RecipesMasterList")
                S.SetMasterRecipes()
            elif(file == "MaterialsMasterList"):
                S.SetMasterMaterials()

def ResetFiles(files=files, d=direc):
    if (input("Would you like to reset all data files? (Y/N)") in "Yy"):
        for x in files:
            fileGen(x)

def checkFile(file, d=direc):
    return os.path.isfile(d + file + '.py')

fixes = []
for x in files:
    if not checkFile(x, direc):
        print(x + " not found! Creating empty version...")
        fixes.append(fileGen(x, direc))

## TODO - Call fileFix on failed import.
        ## AttributeError
from . import StaticData
from . import DynamicData
from . import DynamicInventory
from . import ItemsMasterList
from . import MaterialsMasterList
from . import RecipesMasterList
from . import UncraftableMasterList

if(len(fixes) != 0):
    print("\n\nSome files were not found. Empty versions have been created to prevent a crash on load.\n\
Despite this, the program may not work if the data files are empty. \n\n")
    if(input("Would you like to fill the data files now? (Y/N)") in "Yy"): fileFix(fixes)
    else: print()
else:
    print("All files found!")

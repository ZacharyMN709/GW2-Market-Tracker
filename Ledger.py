import Seeder
import Trawler
import Parser

items, recipes, merchant, inventory = Seeder.SeedLists()
API, baseURL, timeout, directory, outputperline, last_buy, last_sell = Seeder.SeedTrawler()

def LoadLists():
    global items
    global recipes
    global merchant
    global inventory
    items, recipes, merchant, inventory = Seeder.SeedLists()

###########################
### Inventory Managment ###
###########################

## TODO: Test Inventory Methods

def PrintInventory():
    for x in inventory: print(Trawler.items.get(x, ("???",""))[0])

def getLowestPrice(ids):
    price = None
    _, _, a, safe = Trawler.VetResponse(Trawler.getPrices(ids))
    if(safe):
        out, vals = Parser.ParseRawSummary(a)
        if(out == "O"): price = int(vals[2])
    p1 = merchant.get(ids, None)
    if(p1 and p1 < price): price = p1
    return price

def AddInventory(ids, p2, q2):
    p1, q1 = inventory.get(ids, (0,0))
    q = q1+q2
    p = ((p1*q1) + (p2*q2))/q
    inventory[ids] = (p, q)

def RemoveInventory(ids, q2):
    p1, q1 = inventory.get(ids, (0,0))
    q = q1-q2
    if(q <= 0):
        if(q < 0): AttemptCraft(ids, -q)
        if(ids in inventory): inventory.pop(ids)
    else:
        inventory[ids] = (p1, q)

def CalcItemCost(ids, qty, r):
    price = 0
    for x in r:
        if((x[0] in inventory) or (AttemptCraft(x[0], x[1]))):
            i = inventory[x[0]]
            price += i[0] * x[1]
        else:
            sub_price = getLowestPrice(x[0])
            if(sub_price): price += sub_price * x[1]
            
    AddInventory(ids, price, qty)
    for x in r: RemoveInventory(x[0], x[1] * qty)
    return price

def AttemptCraft(ids, qty, rec=None):        
    if ids not in recipes:
        _, d = Trawler.TrawlRecipe(ids, prt=False)
        if(not d):
            print("Item with id " + str(ids) + " not craftable!")
            return False
        else: recipes[ids] = d

    success = False
    d = recipes[ids]
    r = None
    if(len(d) == 1): r = d[list(d.keys())[0]]
    elif(rec != None): r = d.get(rec, None)
    else: print("Multiple craftng recipes possible. \n   FIX THIS!")

    if(r): success = (CalcItemCost(ids, qty, r) != None)
    else: print("Not a valid recipe.")
    
    return success


def CraftItem(ids, qty, lb=last_buy, ls=last_sell, rec=None, inventory=inventory, recipes=recipes):
    ## TODO - When exapanding to multi-threading, ensure no inventory clashes.
    Seeder.SetInventoryList()
    inv_backup = dict(inventory)
    rec_len = len(recipes)
    if(AttemptCraft(ids, qty, rec)):
        if( True ): pass
        else:
            Seeder.WriteInventoryList(inventory, lb, ls)
        if(rec_len < len(recipes)): Seeder.WriteDynamicLists(items, recipes)
    else:
        inventory = inv_backup
        print("Error while crafting item. Reverting to old list.")

def UpdateInventory(buys, sells):
    for x in buys: AddInventory(x, buys[x][0], buys[x][1])
    for x in sells: RemoveInventory(x, sells[x][1])
    return inventory

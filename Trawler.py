from client import GuildWars2Client
import urllib3.exceptions as U3
import requests.exceptions as REQ
import re
import time
import os
import importlib
import Parser
import Looper
import Ledger
import Seeder


## https://status.gw2efficiency.com/ - API Status

########################################
### Data Initialization and Funtions ###
########################################
API, baseURL, timeout, directory, outputperline, last_buy, last_sell = Seeder.SeedTrawler()
if(API == ""): API = None
gw2 = GuildWars2Client(api_key=API)


items, recipes, merchant, inventory = Seeder.SeedLists()
master_items, master_recipes, master_uncraftables, master_materials = Seeder.SeedMaster()


def LoadLists():
    global items
    global recipes
    global merchant
    global inventory
    items, recipes, merchant, inventory = Seeder.SeedLists()

def LoadMasters():
    global master_items
    global master_recipes
    global master_uncraftables
    global master_materials
    master_items, master_recipes, master_uncraftables, master_materials = Seeder.SeedMaster()
    
########################################



####################################
### Connection and Data Safeties ###
####################################
def ConnSafety(methodToRun, ids=None, url=None, retry=True, forceloop=False):
    s = ""
    try:
        if(url): s = methodToRun(id=ids, url=url, timeout=timeout)
        elif(ids): s = methodToRun(id=ids, timeout=timeout)
        else: s = methodToRun(timeout=timeout)
        retry = False
    except ConnectionError: print("\nConnection Error Handled - VAN")
    except U3.ConnectionError: print("\nConnection Error Handled - U3")
    except REQ.ConnectionError: print("\nConnection Error Handled - REQ")
    except ConnectionResetError: print("\nConnection Reset Error Handled")
    except TimeoutError: print("\nTimeout Error Handled")
    except NameError: print("\nName Error Handled")
    except Exception as e: print("\nException caught:\n" + str(e))
    except: print("\nUnknown exception caught!")
    finally:
        if(retry):
            if(forceloop):
                s = ConnSafety(methodToRun, ids=ids, url=url, retry=True, forceloop=True)
                print("CAUTION! MAY BE STUCK IN INFINITE LOOP!")
            else: s = ConnSafety(methodToRun, ids=ids, url=url, retry=False)
    return s

def VetResponse(s):
    out = "?"
    a = str(s)
    safe = True
    
    if(a == ""): out = "!"
    elif(a == "{'text': 'no such id'}"): out = "U"
    elif(a == "[]"): out = "U"
    elif(a == "{}"): out = "U"
    elif(a == "{'text': 'API not active'}"): out = "D"
    elif(a == "{'text': 'too many requests'}"): out = "S"

    if(out != "?"): safe = False
    return out, s, a, safe
##############################################



###############################
### Formatting and Printing ###
###############################
def LinePrint(s, c, m=outputperline):
    space = "   "
    if(c % m == 0): space = "\n"
    print(s, end=space)

def IterPrint(out, count):
    if(count % 25 == 0): out += " "
    if(count % 50 == 0): out += str(count) + '\n'
    print(out, end="")
    return out

def getTime(): return time.asctime( time.localtime(time.time()) )
def getTimestamp(): return '"' + getTime() + '",'
##############################################



#####################################
### API Accessors and File Checks ###
#####################################
def getRecipe(ids, forceloop=False):
        return ConnSafety(gw2.recipes.get, ids=ids, forceloop=forceloop)
def searchRecipeByOutput(ids, forceloop=False):
        return ConnSafety(gw2.recipesbyitem.get, ids=ids,
            url=baseURL+'recipes/search?output='+str(ids), forceloop=forceloop)
def searchRecipeByInput(ids, forceloop=False):
        return ConnSafety(gw2.recipessearch.get, ids=ids,
            url=baseURL+'recipes/search?input='+str(ids), forceloop=forceloop)
def getItem(ids, forceloop=False):
        return ConnSafety(gw2.items.get, ids=ids, forceloop=forceloop)
def getPrices(ids, forceloop=False):
        return ConnSafety(gw2.commerceprices.get, ids=ids, forceloop=forceloop)
def getListings(ids, forceloop=False):
        return ConnSafety(gw2.commercelistings.get, ids=ids, forceloop=forceloop)
def getBuys(forceloop=False):
    return ConnSafety(gw2.commercetransactionsbought.get)
def getSells(forceloop=False):
    return ConnSafety(gw2.commercetransactionssold.get)
def checkAPI():
        s = ConnSafety(gw2.tokeninfo.get)
        if(str(s) == "{'text': 'API not active'}"): return False
        else: return True


def checkFile(ids, pre, suf, d=directory):
    return os.path.isfile(d + str(ids) + pre + suf)

def ListFiles(lst, output=False, d=directory):
    count = 0
    found = []
    t = getTime()+": "
    pre = ['-summary-', '-listings-']
    suf = ['raw.txt', 'cleaned.txt']
    for x in lst:
        series = []
        for p in pre:
            for s in suf:
                count += 1
                f = checkFile(x, p, s, d)
                series.append(f)
                if(output): LinePrint((str(x) + ": " + str(f)), count)
        found.append(series)
    return found


def AppendFiles(lst, filesFrom='TextFiles - Copy/', filesTo='TextFiles/'):
    t = getTime()+": "
    pre = ['-summary-', '-listings-']
    suf = ['raw', 'cleaned']
    typ = ['.txt', '.gdoc']
    for x in lst:
        for p in pre:
            for s in suf:
                try:
                    with open(filesFrom + str(x) + p + s + typ[1], 'r') as f:
                        data1 = f.readlines()
                        out = str(x) + p + s + typ[1]
                        with open(filesTo + str(x) + p + s + typ[1], 'a') as e:
                            print("Writing: " + out)
                            e.write("".join(data1))
                except FileNotFoundError:
                    pass
##############################################



#####################
### Data Trawlers ###
#####################
def TrawlData(ids, timestamp, out, typ, raw, getter, writer, direc=directory):
    pre = ""
    if(out == "S"): pre = "-summary-"
    elif(out == "L"): pre = "-listings-"
    t_out, s, a, safe = VetResponse(getter(ids))
    out = out + ":" + t_out
    
    if(safe):
        if(raw):
            with open(direc + str(ids)+ pre + 'raw' + typ, 'a') as f:
                f.write(timestamp + a + '\n')
        with open(direc + str(ids)+ pre + 'cleaned' + typ, 'a') as f:
            t_out = writer(a, f, timestamp)
            out = out[:-1] + t_out
    return out

def TrawlSummary(ids, timestamp, typ=".txt", raw=False):
    return TrawlData(ids, timestamp, "S", typ, raw, getPrices, Parser.WriteCleanSummary)
def TrawlSummaryToGDoc(ids, timestamp, raw=False):
    return TrawlSummary(ids, timestamp, typ=".gdoc", raw=False)
def TrawlListings(ids, timestamp, typ=".txt", raw=False):
    return TrawlData(ids, timestamp, "L", typ, raw, getListings, Parser.WriteCleanListings)
def TrawlListingsToGDoc(ids, timestamp, raw=False):
    return TrawlListings(ids, timestamp, typ=".gdoc", raw=False)

def TrawlMarket(lst, listings=False, raw=False):
    count = 0
    t = getTimestamp()
    for x in lst:
        count += 1
        out = TrawlSummary(x, t, raw=raw)
        if(listings): out = out + " " + TrawlListings(x, t, raw=raw)
        LinePrint((str(x) + "- " + out), count)
    if(count % 4 != 0): print()
    print()


def TrawlPurchases():
    if(API == None):
        print("API required for functionality!")
        return

    def CompressPurchases(d, time):
        out = dict()
        for x in d:
            if(x['purchased'] <= time): break
            if(x['item_id'] in master_materials or x['item_id'] in items):
                ids, p, q = int(x.get('item_id')), int(x.get('price')), int(x.get('quantity'))
                if(ids in out):
                    p1, q1 = out[ids]
                    p2, q2 = p, q
                    q = q1 + q2
                    p = ((p1*q1) + (p2*q2))/q
                    inventory[ids] = (p, q)
                else: out[ids] = (p, q)
        return out
    
    buys, sells = dict(), dict()
    b, s = getBuys(), getSells()
    lb, ls = b[0].get('purchased'),s[0].get('purchased')
    if((last_buy != None) or (last_sell != None)):
        buys, sells = CompressPurchases(b, last_buy), CompressPurchases(s, last_sell)
    return buys, sells, lb, ls

###############################################



#######################
### Struct Trawlers ###
#######################
def TrawlItem(ids, forceloop=False, prt=False):
    l = []
    out, s, a, safe = VetResponse(getItem(ids, forceloop=False))
    
    if(safe):
        l.append(s.get('name'))
        l.append(s.get('icon'))
        l.append('NoSell' not in s.get('flags'))
        if(len(l) == 3): out = "O"
        else: out = "1"
    out = "I:"+out
    return out, tuple(l)


def TrawlRecipe(ids, prt=True, forceloop=False):
    d = dict()
    out, s, a, safe = VetResponse(searchRecipeByOutput(ids, forceloop=False))

    if(safe):
        out, d = Parser.ParseRecipe(s)
        if d:
            recipes[ids] = d
    out = "R:" + out
    if(prt): print(out, end="")
    return out, d


def TrawlCraftingTree(ids, tree=False):
    print("Trawling Recipes and Items...")

    def getDynamData(ids, tree, spaces=0):
        new_items = dict()
        new_recipes = dict()
        final_out = []
        item_out, l = TrawlItem(ids)
        new_items[ids] = l
        out, d = TrawlRecipe(ids, prt=False)
        if(d): new_recipes[ids] = d
        for y in d:
            for z in d.get(y):
                o, n, i = getDynamData(z[0], tree, spaces+2)
                if n: new_recipes.update(n)
                if i: new_items.update(i)
                final_out += o
        
        fout = str(ids) + "- " + out + " " + item_out
        if(tree):
            if(spaces >= 2): print(" "*(spaces-2) + "v-" + fout)
            else: print(fout)
        else:
            if("O" in out or "U" in out): print(".", end="")
            else: print("!", end="")
        final_out.append(fout)
        return final_out, new_recipes, new_items


    def CharCheck(s):
        c1, c2 = s[-1], s[-5]
        error = (c1 in "D12!?") or (c1 in "D12!?")
        return error


    f_out, recipes, items = getDynamData(ids, tree=tree)
    f_out.sort(reverse=True)
    count = 0
    out = "O"
    print()
    for x in f_out:
        count += 1
        if(CharCheck(x)): out = "!"
        space = "   "
        if(not tree):
            LinePrint(str(x), count)

    print()
    return out, recipes, items
#############################################


####################
### Master Lists ###
####################
def TrawlAllItems(start=None, end=None):
    ## Convert file to utf-8
    def AttemptItemTrawl(ids, count):
        out, item = TrawlItem(ids, forceloop=True)
        out = out[-1]
        if(out == "O"):
            out = "."
        elif(out == "S"):
            print("\n" + "Request Limit Reached at Count: " + str(count))
            print(getTime() + "Sleeping thread. Attempting to continue in 30 seconds." + "\n")
            time.sleep(30)
            return AttemptItemTrawl(ids, count)
        elif(out in "U12"):
            out = "!"

        return out, item

    global master_items
    count = 0
    direc = "DataFiles/"
    if(not os.path.exists(direc)): direc = ""
    lst = ConnSafety(gw2.items.get)
    lst.sort()
    char = len(str(lst[-1]))
    if(start):
        lst = lst[start-1:]
        count = start-1
    if(end):
        lst = lst[:end]

    print("Items in list: " + str(len(lst)))
    with open(direc + 'ItemsMasterList - Log.txt', 'w') as l:
        l.write(getTime() + '\n')
    with open(direc + 'ErrantItems.txt', 'w') as e:
        e.write(getTime() + '\n')
        
    for x in lst:
        out = "?"
        count += 1
        if x in master_items:
            out = ","
        else:
            out, item = AttemptItemTrawl(x, count)
            if(out == "."):
                master_items[x] = item[0]
            else:
                with open(direc + 'ErrantItems.txt', 'a') as e:
                    e.write(str(count) + "-" + str(x) + ": " + str(items) + "\n")
        with open(direc + 'ItemsMasterList - Log.txt', 'a') as l:
            l.write(IterPrint(out, count))
    return master_items


def TrawlAllRecipes(start=None, end=None):
    ## Todo - Change file writing logic to coincide with folder changes
    def AttemptRecipeTrawl(ids, count):
        out, recipe = TrawlRecipe(ids, prt=False, forceloop=True)
        out = out[-1]
        if(out in "OU"):
            out = "."
        elif(out == "S"):
            print("\n" + "Request Limit Reached at Count: " + str(count))
            print(getTime() + "Sleeping thread. Attempting to continue in 30 seconds." + "\n")
            time.sleep(30)
            return AttemptRecipeTrawl(ids, count)
        elif(out in "12"):
            out = "!"

        return out, recipe
    
    count = 0
    direc = "DataFiles/"
    if(not os.path.exists(direc)): direc = ""
    lst = ConnSafety(gw2.items.get)
    lst.sort()
    char = len(str(lst[-1]))
    if(start):
        lst = lst[start-1:]
        count = start-1
    if(end):
        lst = lst[:end]
    print("Items in list: " + str(len(lst)))

    with open(direc + 'ErrantRecipes.txt', 'w') as e:
        e.write(getTime() + '\n')
    with open(direc + 'RecipeMasterList - Log.txt', 'w') as l:
        l.write(getTime() + '\n')

    for x in lst:
        out = "?"
        count += 1
        key = (char-len(str(x)))*" " + str(x)
        if((x in master_recipes)): out = ","
        elif(x in master_uncraftables): out = ","
        else:
            out, recipe = AttemptRecipeTrawl(x, count)
            if(out == "."):
                if(recipe): master_recipes[x] = recipe
                else: master_uncraftables.add(x)
            else:
                with open(direc + 'ErrantRecipes.txt', 'a') as e:
                    e.write(str(count) + "-" + str(x) + ": " + str(recipe) + "\n")
        with open(direc + 'RecipeMasterList - Log.txt', 'a') as l:
            l.write(IterPrint(out, count))
    return master_recipes, master_uncraftables
         

def TrawlAllMaterials():
    crafting_materials = set()
    for x in master_recipes:
        for y in master_recipes[x]:
            for z in master_recipes[x][y]:
                crafting_materials.add(z[0])    


import re
import time
import Seeder
import Trawler


items, recipes, merchant, inventory = Seeder.SeedLists()

def ParseCleanedSummaries():
    pass

def ParseCleanedListings():
    pass


## TODO - Implement current crafted market price when pandas is added
def GetCraftPrice(ids, time):
    cost = 999999999
    if ids in recipes:
        d = recipes.get(ids)
        for x in d:
            subcost = 0
            for y in d.get(x):
                subcost += GetCraftPrice(y[0], time) * y[1]
            if(cost > subcost): cost = subcost
        buy = 1000000##data[ids][time][2]
        if buy:
            if(cost > buy): cost = buy
    else: cost = 1000000##data[ids][time][2]
    if ids in merchant:
        if (cost > merchant.get(ids)): cost = merchant.get(ids)
    return cost


def GetDamaskPrice(time):
    cloth = GetCraftPrice(46741, time)
    square = GetCraftPrice(46739, time)
    cost = cloth + square
##    buy = data[ids][time][2]
##    if buy:
##         if(cost > data[ids][time][2]): cost = data[ids][time][2]
    return cost, cloth, square


def WriteCleanSummary(s, f, t):
    out, vals = ParseRawSummary(s)
    if(out == "O"): f.write(t + ",".join(vals) + '\n')
    return out
    
def WriteCleanListings(s, f, t):
    out, ids, buy, sell = ParseRawListings(s)
    if(out == "O"):
        f.write(t + ids + ',')
        f.write('"buys: ",' + ",".join(buy) + ',')
        f.write('"sells: ",' + ",".join(sell) + '\n')
    return out


def ParseRecipe(s):
    out = "O"
    r = ".*'output_item_id': (\d*),.*'ingredients': \[(.*)\],.*'id': (\d*).*"
    r2 = "{'item_id': (\d*), 'count': (\d*)}"
    r = re.compile(r)
    r2 = re.compile(r2)
    d = dict()
    for x in s:
        c = Trawler.getRecipe(x)
        p = r.search(str(c))
        if p:
            temp = r2.findall(p.group(2))
            i = [(int(x[0]), int(x[1])) for x in temp]
            if i:
                d[int(p.group(3))] = i
            else: out = "2"
        else: out = "1"
    return out, d


## Depreciated - Opting to get data via dictionary reference;
def ParseItem(s):
    out = "O"
    l = []
    r = "{'name': '([^,]*)',.*'icon': '(.*)'}"
    r = re.compile(r)
    p = r.search(s)
    if p:
        l = p.groups()
    else:
        out = "1"
        print(s)
    return out, l


def ParseRawSummary(s):
    out = "O"
    vals = []
    r = "(.)*'id': (\d*),.*'buys': \{(.*)\}, 'sells': \{(.*)\}"
    r2 = "'quantity': (\d*), 'unit_price': (\d*)"
    r = re.compile(r)
    p = r.search(str(s))
    if p:
        r2 = re.compile(r2)
        buy = r2.search(p.group(3))
        sell = r2.search(p.group(4))
        if buy and sell:
            vals = [p.group(2)] + list(buy.groups()) + list(sell.groups())
        else: out = "2"
    else: out = "1"
    return out, vals


def ParseRawListings(s):
    out = "O"
    buy = []
    sell = []
    r = "(.)*'id': (\d*),.*'buys': \[(.*)\], 'sells': \[(.*)\]"
    r2 = "{'listings': (\d*), 'unit_price': (\d*), 'quantity': (\d*)}"
    r = re.compile(r)
    p = r.search(str(s))
    if p:
        ids = p.group(2)
        r2 = re.compile(r2)
        buy_temp = r2.findall(p.group(3))
        sell_temp = r2.findall(p.group(4))
        if buy_temp and sell_temp:
            buy = [",".join(x) for x in buy_temp]
            sell = [",".join(x) for x in sell_temp]
        else: out = "2"
    else: out = "1"
    return out, ids, buy, sell

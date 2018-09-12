import time
import Seeder
import Trawler
import Parser

starttime = time.time()
looptime = 300.0
timefactor = 5

items, recipes, merchant, inventory = Seeder.SeedLists()

   
def Trawl(lst):
    x = 0;
    Seeder.SetInventoryList()
    while True:
        x += 1;
        print(time.asctime( time.localtime(time.time()) ) + ": " + "Loop #" + str(x))
        if(Trawler.checkAPI()):
            Trawler.TrawlMarket(lst, listings=True, raw=True)
            if(x % 24): Seeder.SetInventoryList()
            time.sleep(looptime - ((time.time() - starttime) % looptime))
        else:
            LoopAPI(close=False)
def Run():
    if (71334 not in items): Seeder.SetDynamicLists(71334)
    Trawl(items)


def API():
    up = Trawler.checkAPI()
    if(up): print("API up and running!")
    else: print("API is currently down!")
    return up
def LoopAPI(close=True):
    shorttime = looptime/timefactor
    print("API Down. Checking every " + str(shorttime) + " seconds.")
    while True:
        print(time.asctime( time.localtime(time.time()) ), end=":   ")
        if(API()):
            if(close): exit(0)
            else: break
        time.sleep(shorttime - ((time.time() - starttime) % shorttime))


def ItemFiles(): Trawler.ListFiles(items)

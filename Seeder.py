from DataFiles import StaticData as SD
from DataFiles import DynamicData as DD
from DataFiles import DynamicInventory as DI
from DataFiles import ItemsMasterList as IM
from DataFiles import RecipesMasterList as RM
from DataFiles import UncraftableMasterList as UC
from DataFiles import MaterialsMasterList as CM
import DataFiles
import importlib

df = [DD.items, DD.recipes, SD.merchant, DI.inventory]
trw = [SD.API, SD.baseURL, SD.timeout, SD.directory, SD.outputperline, DI.last_buy, DI.last_sell]
di = [DI.inventory, DI.last_buy, DI.last_sell]
master = [IM.master_item_list, RM.master_recipe_list, UC.uncraftables, CM.crafting_materials]


def SeedLists():
    importlib.reload(SD)
    importlib.reload(DD)
    importlib.reload(DI)
    global df
    df = [DD.items, DD.recipes, SD.merchant, DI.inventory]
    return df[0], df[1], df[2], df[3]

def SeedTrawler():
    importlib.reload(SD)
    importlib.reload(DI)
    global trw
    trw = [SD.API, SD.baseURL, SD.timeout, SD.directory, SD.outputperline, DI.last_buy, DI.last_sell]
    return trw[0], trw[1], trw[2], trw[3], trw[4], trw[5], trw[6]

def SeedInventory():
    importlib.reload(DI)
    global di
    di = [DI.inventory, DI.last_buy, DI.last_sell]
    return di[0], di[1], di[2]

def SeedMaster():
    importlib.reload(IM)
    importlib.reload(RM)
    importlib.reload(UC)
    importlib.reload(CM)
    global master
    master = [IM.master_item_list, RM.master_recipe_list, UC.uncraftables, CM.crafting_materials]
    return master[0], master[1], master[2], master[3]


import Trawler
import Ledger

def SetStaticLists(first=False):
    API, baseURL, timeout, directory, outputperline, _, _ = SeedTrawler()
    merchant_list = [(str(m) + ": " + str(recipes.get(m))) for m in SD.merchant]
    def UserSelectStatic():
        ## TODO: Prompt user to set-up their static data
        ## Set API, and optionally outputperline and timeout
        ## Give option to skip directory
        DataFiles.WriteStaticLists(API, baseURL, timeout, directory, outputperline, merchant_list)          
        Trawler.LoadLists()
        
    if(first):
        UserSelectStatic()
    else:
        overwrite = False
        ## TODO: Warn user of overwiting
        if(overwrite): UserSelectStatic()
        else: print("Overwriting of StaticData.py aborted.")


def SetDynamicLists(item, tree=False):
    ### Sigil of Strength: SetDynamicLists(24562) ###
    ### Damask Patch: SetDynamicLists(71334)      ###
    ### +5 Agony Infusion: SetDynamicLists(49428) ###
    out, r, i = Trawler.TrawlCraftingTree(item, tree)
    if(out == "O"):
        i.update(DD.items)
        r.update(DD.recipes)
        DataFiles.WriteDynamicLists(i, r)
        Trawler.LoadLists()
        Ledger.LoadLists()
    else:
        print("An error has occured. The data is likely corrupt or incorrect.")
        print("DynamicData.py has not been ovewritten.")

def SetInventoryList():
    buys, sells, last_buy, last_sell = Trawler.TrawlPurchases()
    inventory = Ledger.UpdateInventory(buys, sells)
    DataFiles.WriteInventoryList(inventory, last_buy, last_sell)
    Trawler.LoadLists()

def SetMasterItems(s=None, e=None):
    master_items = Trawler.TrawlAllItems(start=s, end=e)
    DataFiles.WriteMasterItems(master_items)
    Trawler.LoadMasters()

def SetMasterRecipes(s=None, e=None):
    recipes, uncraftables = Trawler.TrawlAllRecipes(start=s, end=e)
    DataFiles.WriteMasterRecipes(recipes)
    DataFiles.WriteMasterUncraftables(uncraftables)
    Trawler.LoadMasters()
    
def SetMasterMaterials():
    materials = Trawler.TrawlAllMaterials()
    DataFiles.WriteMasterUncraftables(materials)
    Trawler.LoadMasters()

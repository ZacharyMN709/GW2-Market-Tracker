import time
welcome = "Welcome to the Guild Wars 2 Market Observer!\n\n\n"

setup = "This setup file will create python files which will \
be used later in the running of the program.\n\n"

text = "In order to have optimal functionality, you should \
provide the program with access to your account through an \
API code.\n\
This code can be generated at:   'TODO'\n\n\
Please be aware the inital set up will take several hours \
to complete due to trawling items and recipes from the server.\n\n\
Also, should you re-run setup, the trawler will skip \
items it has already trawled from the server - making set-up \
much faster. \n\
Please keep in mind that this means in order to \
get a fresh verion of the master lists, you will have to manually \
delete them and trawl all the data over again. This will likely \
only be required after a GW2 update which **changes** item or \
recipe ids.\n\n"

warning = "Trawling will commence shortly.\n\
If there are no errors in submitted data, setup will close \
automatically."

def TextCrawl(s, t):
    for x in s:
        print(x, end="")
        if(x is not "\n"): time.sleep(t)

def Countdown(s): TextCrawl(s, 1)
def CrawlCrawl(s): TextCrawl(s, 0.1)
def SlowCrawl(s): TextCrawl(s, 0.05)
def FastCrawl(s): TextCrawl(s, 0.025)
def HyperCrawl(s): TextCrawl(s, 0.000001)


SlowCrawl(welcome)
FastCrawl(setup)
HyperCrawl(text)
CrawlCrawl("Setup Starting in:\n")
Countdown("3\n2\n1\n\n\n\n")

'''
Setup Order:
Reset Files
Get StaticData info
Set StaticData
Get DynamicData info
Set Master Lists
Check DyanamicData info for validity
Set Dynamic Lists
Set Personal Inventory
'''

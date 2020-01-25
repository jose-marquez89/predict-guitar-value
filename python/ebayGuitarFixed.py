# ebayGuitarScrape.py - Scrapes data from ebay.com on sold and completed 
# electric guitar listings. Uses multi threading to get 100 links per page

from bs4 import BeautifulSoup
import requests 
import logging
import threading
import csv
import re

logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s - %(levelname)s - %(message)s")

guitarCsv = open('guitars.csv', 'w')
writer = csv.writer()

# Write initial columns for csv
columns = ('Accessories', 'Body Color', 'Body Material', 'Body Type', 'Brand', 
           'Bundle Description', 'Color', 'Condition', 'Country of Manufacture', 
           'Country/Region of Manufacture', 'Custom Bundle', 'Dexterity', 
           'Features', 'Fingerboard', 'Hand', 'Items Included', 'MPN', 'Model', 
           'Model Year', 'Modification Description', 'Modified Item', 'Neck', 
           'Non-Domestic Product', 'Pickup', 'Product Line', 'Product Type', 
           'Right-/ Left-Handed', 'Serial Number', 'Series', 'Size', 
           'Soundboard Style', 'String Configuration', 'Style', 'Type', 'UPC', 
           'serial number', 'Price')
writer.writerow(columns)

threadList = []
# Main page with filters for 6, 7, 8, 9 and 12 string guitars
mainUrl = "https://www.ebay.com/sch/i.html?_fsrp=1&_sop=13&_nkw="\
          "electric+guitar&_sacat=3858&LH_Complete=1&LH_Sold=1&Size="\
          "Full%2520Size%7C%21&LH_PrefLoc=1&_ipg=100&_oaa=1&rt="\
          "nc&String%2520Configuration=9%2520String%7C7%2520String%"\
          "7C8%2520String%7C6%2520String%7C12%2520String&_dcat=33034"

def writeItemInfo(targetCsv, itemHref):
    '''
    Function opens individual item links, 
    arranges item details sequentially and 
    writes a row to the target csv file'''

    item = requests.get(itemHref)
  
    threadWriter = csv.writer(targetCsv)


    # Parse item page HTML
    itemSoup = BeautifulSoup(item.text)

    # Select table with item details
    infoBox = itemSoup.select('.section')

    if len(infoBox) == 0:
        logging.info(f"Unwanted Link: {itemHref}")
        return None

    # Parse HTML in attribute table
    tableSoup = BeautifulSoup(str(infoBox[0]))

    # Get all attribute elements
    allDetails = tableSoup.select('td')

    # Item details to populate, some will be empty
    details = {'Accessories': '', 'Body Color': '', 'Body Material': '',
               'Body Type': '', 'Brand': '', 'Bundle Description': '',
               'Color': '', 'Condition': '', 'Country of Manufacture': '',
               'Country/Region of Manufacture': '', 'Custom Bundle': '', 
               'Dexterity': '', 'Features': '', 'Fingerboard': '',
               'Hand': '', 'Items Included': '', 'MPN': '', 'Model': '',
               'Model Year': '', 'Modification Description': '',
               'Modified Item': '', 'Neck': '', 'Non-Domestic Product': '',
               'Pickup': '', 'Product Line': '', 'Product Type': '', 
               'Right-/ Left-Handed': '', 'Serial Number': '', 'Series': '',
               'Size': '', 'Soundboard Style': '', 
               'String Configuration': '', 'Style': '','Type': '', 'UPC': '',
               'serial number': '', 'Price': ''}
  
    # Set current item attribute
    current = None
  
    # Get details into detail dictionary
    for element in allDetails:
        listItem = element.getText().strip().strip(':')
  
        # Set special conditions when "Condition" is absent
        if listItem.lower().startswith('used'): 
            myDict['Condition'] = listItem[:4].title()
        elif listItem.lower().startswith('new'):
            myDict['Condition'] = listItem[:3].title()
        elif listItem.startswith('“'):
            continue
        else:
            # Set attribute labels that match details as current label
            if listItem in myDict.keys():
                current = listItem
                continue
            # If label exists, set value in detail dictionary
            if current != None:
                myDict[current] = listItem
                saved += 1
                current = None
            # Skip attribute detail if attribute not in detail dictionary
            else:
                continue
  
        # Get item price as float
        rawPrice = itemSoup.select('.notranslate')[0].getText()
        price = float(re.sub(r'[^0-9\.]', '', rawPrice))
        details['Price'] = price

  


# Get main page with pre-selected filters
mainPage = requests.get(mainUrl)
try:
    mainPage.raise_for_status
except Exeption as err:
    logging.error(err)

# Parse HTML on main page
mainSoup = BeautifulSoup(mainPage.text)

# Select item links on page
itemLinks = mainSoup.select('.s-item__link')
logging.info(f"Item links on page: {len(itemLinks)}")

for itemLink in itemLinks:
    threadObj = threading.Thread(target=writeItemInfo, 
                               args=(guitarCsv, itemLink.get('href')))
    threadList.append(threadObj)
    threadObj.start()

# Wait for all threads to end
for thread in threadList:
    thread.join()   
logging.info("Process Complete.")


############ FOR 100 RESULTS #######################
# TODO: Start 100 threads for the current page     #
# TODO: Wait for all threads to end                # 
# TODO: Close csv file                             #
####################################################

############ FOR ALL RESULTS #######################
# TODO: Find number of results                     #
# TODO: Calculate number of pages to visit         # 
# TODO: Start 100 threads for each of 100 pages    #
# TODO: Wait for 1000 threads to finish and repeat #
# TODO: When jobs == results, stop and close csv   # 
####################################################


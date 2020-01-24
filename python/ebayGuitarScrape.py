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

	

	# Parse item page HTML
	itemSoup = BeautifulSoup(item.text)
    
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
	current = None
	skip = 0
	saved = 0
	for e in test:
  		listItem = e.getText().strip().strip(':')
  		attributes.append(listItem)
  
  	if listItem.lower().startswith('used'): 
    	myDict['Condition'] = listItem[:4].title()
  	elif listItem.lower().startswith('new'):
    	myDict['Condition'] = listItem[:3].title()
  	elif listItem.startswith('“'):
    	continue
  	else:
    	if listItem in myDict.keys():
      		current = listItem
      		continue
    	if current != None:
      		myDict[current] = listItem
      		saved += 1
      		current = None
    else:
      continue
	
	# Get item price as float
	rawPrice = itemSoup.select('.notranslate')[0].getText()
	price = float(re.sub(r'[^0-9\.]', '', rawPrice))
	details['Price'] = price

	# TODO: Identify unwanted links
	# TODO: Extract desired link from unwanted page
	# TODO: Get main specification table
	# TODO: Store Specifications in "itemDetails"
	# TODO: Write a csv row to the target file


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


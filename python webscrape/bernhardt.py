from selenium import webdriver 
from bs4 import BeautifulSoup
import pandas as pd
import csv
import urllib.request
from lxml import html
import time
from selenium.webdriver.support.ui import WebDriverWait
from pprint import pprint as pp

scrape_urls = "Classic-Imports-and-Design\python webscrape\url-lists\Bernhardt.csv"
print('Name of Output CSV File')
filename = input()

file = open(filename+'.csv', 'w')
file.truncate()
writer = csv.writer(file)

driver = webdriver.Chrome("Classic-Imports-and-Design\python webscrape\chromedriver.exe")

#login
driver.get('https://dealerportal.bernhardt.com')
print("Please log into the wholesale account.")
input()

with open(scrape_urls) as f:
    reader = csv.reader(f)
    scrape_urls = list(reader)

for product in scrape_urls:

    print(product[0])
    print(product[1])
    row = 1
    data = []
    print("Establishing connection to > " + product[0])
    try:
        driver.get("https://dealerportal.bernhardt.com/shop/" + product[0].strip().replace('-','') + '?Search=' + product[0].strip())
        time.sleep(3)
        content = driver.page_source
        soup = BeautifulSoup(content, "html.parser")
        tree = html.fromstring(driver.page_source) 
    except:
        print('ERROR!!!!!!! @46')
        continue

    print("Scraping Information...")
    #SKU
    sku = tree.xpath('/html/body/div[1]/div[1]/section[2]/div/div/div/div/div/ui-view/shopping-container/div/ui-view/shopping-one-up/div[3]/div[1]/div[2]/div[3]/div[1]/span').text
    data.append(sku)
    #title
    title = tree.xpath('/html/body/div[1]/div[1]/section[2]/div/div/div/div/div/ui-view/shopping-container/div/ui-view/shopping-one-up/div[2]/div[2]/h1').text
    data.append(title)
    #brand
    data.append('Bernhardt')
    #category
    data.append('_')
    #price
    data.append('$')
    data.append('R$')
    #description
    product_desc = tree.xpath('/html/body/div[1]/div[1]/section[2]/div/div/div/div/div/ui-view/shopping-container/div/ui-view/shopping-one-up/div[3]/shopping-one-up-details/div/div/div[1]/div/div/p/text()')
    data.append(product_desc)
    #dimensions
    w = tree.xpath('/html/body/div[1]/div[1]/section[2]/div/div/div/div/div/ui-view/shopping-container/div/ui-view/shopping-one-up/div[3]/shopping-one-up-details/div/div/div[3]/div/panel/div/div[2]/div[1]/div[1]/ul/li[2]').text
    d = tree.xpath('/html/body/div[1]/div[1]/section[2]/div/div/div/div/div/ui-view/shopping-container/div/ui-view/shopping-one-up/div[3]/shopping-one-up-details/div/div/div[3]/div/panel/div/div[2]/div[1]/div[2]/ul/li[2]').text
    h = tree.xpath('/html/body/div[1]/div[1]/section[2]/div/div/div/div/div/ui-view/shopping-container/div/ui-view/shopping-one-up/div[3]/shopping-one-up-details/div/div/div[3]/div/panel/div/div[2]/div[1]/div[3]/ul/li[2]').text
    #images
    pp(data)
    writer.writerow(data)
    print("Item " + sku + " written to CSV table.")
    
file.close()
driver.close()

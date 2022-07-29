from selenium import webdriver 
from bs4 import BeautifulSoup
import pandas as pd
import csv
import urllib.request
from lxml import html
import time

scrape_urls = "url-lists/caracole-urls.csv"
print('Name of Output CSV File')
filename = input()

file = open(filename+'.csv', 'w')
file.truncate()
writer = csv.writer(file)

driver = webdriver.Chrome("chromedriver.exe")

#login
driver.get('https://my.furnishweb.com/index.cfm?go=products.show')
print("Please log into the wholesale account.")
input()

with open(scrape_urls) as f:
    reader = csv.reader(f)
    scrape_urls = list(reader)

for product in scrape_urls:
    print(product[0])
    #print(product[1])
    row = 1
    data = []
    print("Establishing connection to > " + product[0])
    driver.get('https://my.furnishweb.com/index.cfm?go=products.show')
    js = "dsp_detail('" + product[0].strip() + "');"
    print(js)
    driver.execute_script(js)
    time.sleep(3)
    content = driver.page_source
    soup = BeautifulSoup(content, "html.parser")
    tree = html.fromstring(driver.page_source) 

    print("Scraping Information...")
    #SKU
    sku = tree.xpath('/html/body/div[1]/div[2]/div/div/div[1]/div/div[3]/div/div[2]/div/div[1]/h2[1]')[0].text
    data.append(sku)
    #Title  
    product_title = tree.xpath('/html/body/div[1]/div[2]/div/div/div[1]/div/div[3]/div/div[2]/div/div[1]/h2[2]')[0].text
    data.append(product_title)
    #Brand
    data.append('Caracole')
    #Category
    #data.append(product[1])
    #Wholesale Price
    wholesale = tree.xpath('/html/body/div[1]/div[2]/div/div/div[1]/div/div[3]/div/div[4]/div[1]/table/tbody[2]/tr[2]/td[2]/text()')[0].strip().lstrip('$')
    data.append(wholesale)
    #Item Description
    product_info = soup.find()
    print(product_info)
    data.append(product_info)
    #Images
    print('Downloading product images...')
#...


    writer.writerow(data)
    print("Item " + product[0] + " written to CSV table.")

driver.close()



from selenium import webdriver 
from bs4 import BeautifulSoup
import pandas as pd
import csv
import urllib.request
from lxml import html
import time
from pprint import pprint as pp
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import DesiredCapabilities

scrape_sku_file = 'python webscrape\\url-lists\\list.csv'

output_file = 'output.csv'
output_file = open(output_file, 'w')
output_file.truncate()
output = csv.writer(output_file)


with open('python webscrape\parameters.csv', 'r') as input_file:
    input_reader = csv.reader(input_file)
    line = 0
    for row in input_reader:
        if line==0:
            wholesale_login_url = row[1]
        if line==1:
            url_prefix = row[1]
        if line==2:
            url_suffix = row[1]
        if line==3:
            carousel_class = row[1]
        line = line + 1
#        if line==4:
#            thumbnail_class = row[1]

with open(scrape_sku_file, 'r') as scrape_sku_file:
    scrape_sku_reader = csv.reader(scrape_sku_file)
    scrape_sku = list(scrape_sku_reader) 

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument = {'user-data-dir' : 'C:\\Users\\Taggart\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 4'}

driver = webdriver.Chrome("python webscrape\chromedriver.exe", options = chrome_options)

#login
driver.get(wholesale_login_url)
print("Please log into the wholesale account.")
input()

item_itr = 1
for sku in scrape_sku:
    sku = str(sku).strip()
    msg = 'Scraping Item  ' + str(sku) + '  | ' + str(item_itr) + ' of ' + str(len(scrape_sku)) + ' | ' + '{:.0%}'.format(item_itr/len(scrape_sku))
    print(msg) 
#, end='\r'

    pp([url_prefix,url_suffix,carousel_class])
    driver.get(url_prefix + sku + url_suffix)
    time.sleep(3)
    content = driver.page_source
    soup = BeautifulSoup(content, "html.parser")
    tree = html.fromstring(driver.page_source) 

    #images
    images = soup.findAll('div', class_=carousel_class)
    for element in images:
        pp(element)

driver.close()
        


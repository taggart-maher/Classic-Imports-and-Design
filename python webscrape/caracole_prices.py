from selenium import webdriver 
 #-*- coding: utf-8 -*-
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import csv
import urllib.request
from lxml import html
import time
from selenium.webdriver.support.ui import WebDriverWait
from pprint import pprint as pp
from fuzzywuzzy import fuzz

scrape_file = 'Classic-Imports-and-Design/python webscrape/url-lists/caracole-sku.csv'
login_url = 'https://my.furnishweb.com/'

with open(scrape_file) as f:
    reader = csv.reader(f, delimiter=',')
    scrape_file = list(reader)

writefile = open('Classic-Imports-and-Design\python webscrape\output.csv', 'w+', encoding='UTF-8')
output_file = csv.writer(writefile, delimiter=",")

driver = webdriver.Chrome('Classic-Imports-and-Design\python webscrape\chromedriver.exe')

#login
driver.get(login_url)
print("Please log into the wholesale account.")
print('regencyantiqmd@aol.com')
print('23Friday!01')
input()

data = ['sku', 'Name', 'Brand', 'Categories', 'Wholesale', 'Retail', 'Description', 'Images', 'Length', 'Width', 'Height']
output_file.writerow(data)
fails = []

for product in scrape_file:
    pp(fails)
    product[0] = product[0].strip()
    product[1] = product[1].strip()
    data = []
    driver.get('https://my.furnishweb.com/index.cfm?go=products.show') 
    driver.execute_script('dsp_detail("' + product[0] + '");')
    time.sleep(3)

    try:
        product_status = driver.find_elements(By.XPATH, '/html/body/div[1]/div[2]/div/div/div[1]/div/div[3]/div/div[2]/div/div[1]/p')[0].text
        if 'discontinued' in product_status.lower():
            fails.append(product[0] + ' is discontinued')
            continue
    except:
        fails.append(product[0] + ' could not find status')
        continue
    #sku
    data.append(product[0])
    #Wholesale
    try:
        price_table = driver.find_elements(By.CLASS_NAME, 'table')[0].text.split('\n')
        index = 0
        for element in price_table:
            if 'Greensboro' in element:
                wholesale = float( price_table[index + 2].lstrip('$').replace(',','') )
                price_found = True
                data.append(wholesale)
                break
            else:
                price_found = False
                index = index + 1
        if price_found == False:
            fails.append(product[0] + ' has no Greensboro price')
            continue
        #Retail
        data.append(wholesale * 2)
    except:
        data.append('0')
        data.append('0')
        fails.append(product[0] + ' does not have price table')
    print(data)

    output_file.writerow(data)



pp(fails)
writefile.close()

#driver.get(url)
#time.sleep()
#content = driver.page_source
#soup = BeautifulSoup(content, "html.parser")
#tree = html.fromstring(driver.page_source) 

#driver.find_elements(By.XPATH, XPATH)
#driver.find_elements(By.CLASS_NAME, CLASSNAME)
#soup.find("TAG-TYPE", class_="CLASS-NAME").text

#urllib.request.urlretrieve(IMG-URL, FILENAME) 

#output_file.writerow(data)
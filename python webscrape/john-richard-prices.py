from selenium import webdriver 
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import pandas as pd
import csv
import urllib.request
from lxml import html
from selenium.webdriver.common.by import By
import time
from pprint import pprint as pp

scrape_file = 'Classic-Imports-and-Design/python webscrape/url-lists/johnrichard-sku.csv'
login_url = 'https://www.johnrichard.com/'
credentials = ['REGFI1','21030']

with open(scrape_file) as f:
    reader = csv.reader(f, delimiter=',')
    scrape_file = list(reader)

writefile = open('outputfile.csv', 'w+', encoding='UTF8')
output_file = csv.writer(writefile, delimiter=",")

driver = webdriver.Chrome('Classic-Imports-and-Design\python webscrape\chromedriver.exe')

#login
driver.get(login_url)
print("Please log into the wholesale account.")
print(credentials[0])
print(credentials[1])
input()

data = ['sku', 'Wholesale', 'Retail']
output_file.writerow(data)

fails = []

itr = 1
for product in scrape_file:
    product[0] = product[0].strip()
    product[1] = product[1].strip()
    pp('Scarping product ' + product[0] + ' | Item ' +  str(itr) + ' / ' + str(len(scrape_file)))
    itr = itr + 1
    data = []
    
    try: 
        driver.get('https://www.johnrichard.com/shop/' + product[0])
    except:
        fails.append(str(itr) + product[0])
        continue
    time.sleep(2.5)
    content = driver.page_source
    soup = BeautifulSoup(content, "html.parser")
    tree = html.fromstring(driver.page_source) 

    #SKU
    data.append(product[0])
    #Wholesale
    try:
        wholesale_price = driver.find_element(By.CSS_SELECTOR, 'p.product-price').find_element(By.CLASS_NAME, 'ng-binding').text.lstrip('$').replace(',','')
        wholesale_price = wholesale_price
        data.append(wholesale_price)
    #Retail
        retail_price = round(float(wholesale_price)*1.1*2.5)
        print(retail_price)
        data.append( retail_price )
    except Exception as err:
        print(err)
        data.append('ERROR')
        data.append('ERROR')
        fails.append(product[0] + ' has no wholesale')
    pp(data)
    pp(fails)
    output_file.writerow(data)

writefile.close()
pp(fails)

#driver.get(url)
#time.sleep()
#content = driver.page_source
#soup = BeautifulSoup(content, "html.parser")
#tree = html.fromstring(driver.page_source) 

#tree.xpath()[0].text (.text needed if end of xpath NOT /text)
#soup.find("TAG-TYPE", class_="CLASS-NAME").text

#urllib.request.urlretrieve(IMG-URL, FILENAME) 

#output_file.writerow(data)
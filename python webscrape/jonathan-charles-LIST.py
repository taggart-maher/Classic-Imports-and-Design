from selenium import webdriver 
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import csv
import urllib.request
from lxml import html
import time
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from pprint import pprint as pp

login_url = 'https://catalog.jonathancharlesfurniture.com/'

writefile = open('Classic-Imports-and-Design\python webscrape\output.csv', 'w+', encoding='UTF8', newline='')
output_file = csv.writer(writefile, delimiter=",")

driver = webdriver.Chrome('Classic-Imports-and-Design\python webscrape\chromedriver.exe')

#login
driver.get(login_url)
print("Please log into the wholesale account.")
print('mklatsky')
print('23Monday!01')
input()

data = ['SKU', 'Catagory']
output_file.writerow(data)
fails = []
active = True

while active == True:
    cat = input('Select a catagory, then provide a name. OR type 000 to terminate: ')
    if cat == '000':
        active == False
        break

    catalog = driver.find_elements(By.CLASS_NAME, 'catalog-item')
    index = 0
    for element in catalog:
        data = []
        element = driver.find_elements(By.CLASS_NAME, 'catalog-item')[index]
        all_info = element.find_elements(By.TAG_NAME, 'li')
        for text in all_info:
            if ' OH' in text.text:
                on_hand = int( text.text.strip().rstrip(' OH') )
            if ' IT' in text.text:
                in_transit = int( text.text.strip().rstrip(' IT') )
        if on_hand > 0 or in_transit > 0:
            sku_link = element.find_element(By.CLASS_NAME, 'catalog-item-number')
            sku = sku_link.text
            if sku[-1] == '.' and sku[-2] == '.' and sku[-3] == '.':
                sku_link.click()
                try:
                    element_present = EC.presence_of_element_located((By.CLASS_NAME, 'item-name'))
                    WebDriverWait(driver, 6).until(element_present)
                except TimeoutException:
                    print(sku + ' TOOK TO LONG')
                sku = driver.find_element(By.CLASS_NAME, 'item-name').find_element(By.TAG_NAME, 'h2').text
                driver.back()
                
            data.append(sku)
            data.append(cat)
            pp(data)
            output_file.writerow(data)        
        index = index + 1

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
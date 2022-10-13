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
from selenium.webdriver.chrome.options import Options
from pprint import pprint as pp
from tabulate import tabulate

scrape_file = r'Classic-Imports-and-Design\python webscrape\url-lists\jonathan-charles-sku.csv'
login_url = 'https://catalog.jonathancharlesfurniture.com/jcusa/e/mobile/login'

with open(scrape_file, encoding='UTF-8') as f:
    reader = csv.reader(f, delimiter=',')
    scrape_file = list(reader)

writefile = open('Classic-Imports-and-Design\python webscrape\output.csv', 'w+', encoding='UTF8', newline='')
output_file = csv.writer(writefile, delimiter=",")

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome('Classic-Imports-and-Design\python webscrape\chromedriver.exe', options=options)

#login
print('mklatsky')
print('23Monday!01')
driver.get(login_url)
print("Please log into the wholesale account.")
input()

file_header = ['sku', 'Wholesale', 'Retail']
output_file.writerow(file_header)
fails = []

for product in scrape_file:
    try:
        product[0] = product[0].strip()
        product[1] = product[1].strip()
        data = []
        driver.get('https://catalog.jonathancharlesfurniture.com/jcusa/e/mobile/products?query=' + product[0])  
        try:
            element_present = EC.presence_of_element_located((By.CLASS_NAME, 'catalog-item-number'))
            WebDriverWait(driver, 6).until(element_present)
        except:
            fails.append(product[0] + ' Does not exist')
            continue
        #click to product page
        driver.find_element(By.CLASS_NAME, 'catalog-item-number').click()
        time.sleep(3)
        #sku
        data.append(product[0])
        
        #wholesale
        try:
            wholesale = float( driver.find_element(By.CLASS_NAME, 'item-price').text.lstrip('$').replace(',','') )
            data.append(wholesale)
        #retail
            data.append(wholesale*2.2)
        except:
            data.append(0)
            data.append(0)
            fails.append(product[0] + ' has NO PRICE')

        pp(fails)
        print_table = data.copy()
        print(tabulate([file_header] + [print_table]))
        output_file.writerow(data)
    except:
        fails.append(product[0] + ' FAILED DUE TO UNKNOWN ERROR')

pp(fails)
writefile.close()

#element_present = EC.presence_of_element_located((By.CLASS_NAME, 'product-item-link'))
#WebDriverWait(driver, 6).until(element_present)
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
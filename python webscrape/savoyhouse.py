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

scrape_file
login_url

with open(scrape_file, encoding='UTF-8') as f:
    reader = csv.reader(f, delimiter=',')
    scrape_file = list(reader)

writefile = open('Classic-Imports-and-Design\python webscrape\output.csv', 'w+', encoding='UTF8', newline='')
output_file = csv.writer(writefile, delimiter=",")

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome('Classic-Imports-and-Design\python webscrape\chromedriver.exe', options=options)

#login
driver.get(login_url)
print("Please log into the wholesale account.")
input()

file_header = ['sku', 'Name', 'Brand', 'Categories', 'Wholesale', 'Retail', 'Description', 'Images', 'GTIN12 / UPC']
output_file.writerow(file_header)
fails = []

for product in scrape_file:
    product[0] = product[0].strip()
    product[1] = product[1].strip()
    data = []
    driver.get('https://portal.savoyhouse.com/shl/e/1/products?query=' + product[0]) 
    
    try:
        element_present = EC.presence_of_element_located((By.CLASS_NAME, 'catalog-item-number'))
        WebDriverWait(driver, 6).until(element_present)
    except TimeoutException:
        fails.append(product[0] + ' Does not appear in search')
        continue
    driver.find_element(By.CLASS_NAME, 'catalog-item-number').click()
    time.sleep(3)

    window = driver.find_element(By.CLASS_NAME, 'product-item')
    #sku
    data.append(product[0])
    #name
    try:
        title = window.find_element(By.TAG_NAME, 'h1').text
        data.append(title)
    except:
        fails.append(product[0] + ' could not grab title')
        continue
    #brand
    data.append('Savoy House')
    #categories
    data.append(product[1])
    #wholesale
    try:
        wholesale = float( window.find_element(By.CLASS_NAME, 'item-price').text.lstrip('$').replace(',','') )
        data.append(wholesale)
    #retail
        data.append(wholesale * 2)
    except:
        fails.append(product[0] + ' failed to grab PRICE')
        data.append('0')
    #description
    try:
        description = window.find_element(By.CSS_SELECTOR, 'p.story-full')
    except:
        fails.append(product[1] + ' could not grab DESCRIPTION')
        data.append('No Description. Call For details 443-330-5715')
    #images
    pp(fails)
    print_table = data.copy()
    print_table[6] = 'desc...'
    print_table[7] = 'images...'
    print(tabulate([file_header] + [print_table]))
    print(data[6])
    print(data[7])
    output_file.writerow(data)

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
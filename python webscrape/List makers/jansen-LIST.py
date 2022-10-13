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

login_url = 'https://jansenfurniture.ca/my-account/'

writefile = open('Classic-Imports-and-Design\python webscrape\output.csv', 'w+', encoding='UTF8', newline='')
output_file = csv.writer(writefile, delimiter=",")

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome('Classic-Imports-and-Design\python webscrape\chromedriver.exe', options=options)

#login
print('regencyantiqmd@aol.com\n23Thursday!01')
driver.get(login_url)
print("Please log into the wholesale account.")
input()

file_header = ['sku', 'Categories']
output_file.writerow(file_header)
fails = []

active = True
while active == True:
    print('Please browse to a catagory page, then type the catagory name. TYPE 000 to FINISH')
    cat = input()
    if cat == '000':
        active = False
        print('fin!')
        continue

    products = driver.find_elements(By.CLASS_NAME, 'woocommerce-LoopProduct-link')
    for element in products:
        data = []
        try:
            sku = element.find_element(By.CLASS_NAME, 'price').text
            data.append(sku)
            data.append(cat)
            print(sku + '  -|-  ' + cat)
        except Exception as err:
            print('something went wrong... ' + err)
            data.append('ERROR')
            data.append('ERROR')
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
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

scrape_file = r'Classic-Imports-and-Design\python webscrape\url-lists\jansen-sku.csv'
login_url = 'https://jansenfurniture.ca/my-account/'

with open(scrape_file, encoding='UTF-8') as f:
    reader = csv.reader(f, delimiter=',')
    scrape_file = list(reader)

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

file_header = ['sku', 'Name', 'Brand', 'Categories', 'Wholesale', 'Retail', 'Description', 'Images']
output_file.writerow(file_header)
fails = []

for product in scrape_file:
    product[0] = product[0].strip()
    product[1] = product[1].strip()
    data = []
    driver.get('https://jansenfurniture.ca/?post_type=product&s=' + product[0]) 
    time.sleep(3)
    #sku
    data.append(product[0])
    #name
    try:
        name = driver.find_element(By.TAG_NAME, 'h1').text.title()
        #sometimes, products with / in the sku do not appear in search
        if name == 'Online Store':
            search_list = driver.find_elements(By.CLASS_NAME, 'woocommerce-LoopProduct-link')
            for element in search_list:
                sku = element.find_element(By.CLASS_NAME, 'price').text
                if sku == product[0]:
                    driver.get( element.get_attribute('href') )
                    time.sleep(3)
                    break
            name = driver.find_element(By.TAG_NAME, 'h1').text.title()
        data.append(name)
    except Exception as err:
        print(err)
        fails.append(product[0] + 'has no title')
        continue
    #brand
    data.append('Jansen Furniture')
    #categories
    data.append(product[1])
    #wholesale
    try:
        wholesale_price = float(driver.find_element(By.CLASS_NAME, 'wholesale_price_container').find_element(By.CLASS_NAME, 'woocommerce-Price-amount').text.replace(',','').lstrip('$')) 
        data.append(wholesale_price)
    #retail
        retail_price = wholesale_price*2
        data.append(retail_price)
    except:
        data.append('ERORR')
        data.append('ERROR')
        fails.append(product[0] + ' could not grab price')
    #description
    description = ''
    dimensions = ''
    try:
        dimensions = driver.find_element(By.CLASS_NAME, 'dimensions-table').text
    except:
        fails.append(product[0] + ' has no dimensions')
    try:
        description = driver.find_element(By.CLASS_NAME, 'et-dynamic-content-woo--product_description').find_element(By.TAG_NAME, 'p').text.capitalize()
    except:
        fails.append(product[0] + ' has no description')
    data.append(dimensions + '\n\n' + description)
    #images
    try:
        carousel = driver.find_element(By.CLASS_NAME, 'woocommerce-product-gallery__wrapper')
        images = carousel.find_elements(By.TAG_NAME, 'a')
        image_urls = []
        image_filenames = []
        c = 1
        for element in images:
            image_filenames.append(product[0].replace('/','-') + '-' + str(c))
            image_urls.append(element.get_attribute('href'))
            c = c+1
        c = 0
        for url in image_urls:
            urllib.request.urlretrieve(url, 'Classic-Imports-and-Design/python webscrape/product-images/' + image_filenames[c] + '.jpg') 
            c = c+1
        data.append(','.join(image_filenames))
    except Exception as err:
        data.append('ERROR')
        fails.append(product[0] + ' could not grab IMAGES \n' + str(err))          

    pp(fails)
    print_table = data.copy()
    print_table[6] = 'desc...'
    print_table[7] = 'images...'
    print(tabulate([file_header] + [print_table]))
    print(data[6])
    print(data[7])
    print('\n\n')
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
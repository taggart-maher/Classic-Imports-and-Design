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


scrape_file = r'Classic-Imports-and-Design\python webscrape\url-lists\eichholtz-sku.csv'
login_url = 'https://eichholtzusa.com/customer/account/login/'

with open(scrape_file, encoding='UTF-8') as f:
    reader = csv.reader(f, delimiter=',')
    scrape_file = list(reader)

writefile = open('Classic-Imports-and-Design\python webscrape\output.csv', 'w+', encoding='UTF8', newline='')
output_file = csv.writer(writefile, delimiter=",")


options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome('Classic-Imports-and-Design\python webscrape\chromedriver.exe', options=options)

#login
print("Please log into the wholesale account.")
print('regencyantiqmd@aol.com')
print('108Alaska!07')
driver.get(login_url)
input()

file_header = ['sku', 'Name', 'Brand', 'Categories', 'Wholesale', 'Retail', 'Description', 'Images']
output_file.writerow(file_header)
fails = []

for product in scrape_file:
    try:
        product[0] = product[0].strip()
        product[1] = product[1].strip()
        data = []
        #Search for product
        try:
            driver.get('https://eichholtzusa.com/catalogsearch/result/?q=' + product[0])
        except: 
            fails.append(product[0] + ' Search did not succeed') 
        #Click search result
        try:
            element_present = EC.presence_of_element_located((By.CLASS_NAME, 'product-item-link'))
            WebDriverWait(driver, 6).until(element_present)
            driver.find_elements(By.CLASS_NAME, 'product-item-link')[0].click()
        except TimeoutException:
            fails.append(product[0] + ' took too long to load')
        #Wait for product page to load
        time.sleep(3)
        #sku
        try:
            info_wrap = driver.find_elements(By.CLASS_NAME, 'product-info-price')[0]
            sku = info_wrap.find_element(By.CLASS_NAME, 'value').text
            data.append(sku)
        #name
            name = driver.find_element(By.CLASS_NAME, 'page-title').text.title()
            data.append(name)
        except:
            fails.append(product[0] + 'has no sku / name')
            continue
        #brand
        data.append('Eichholtz')
        #Catagories
        data.append(product[1])
        #wholesale
        try:
            wholesale = float( info_wrap.find_elements(By.TAG_NAME, 'meta')[0].get_attribute('content') )
            data.append(wholesale)
            #retail
            data.append(wholesale*2.5)
        except:
            fails.append(product[0] + ' has no price')
            data.append(0)
            data.append(0)
        #description & DIMENSIONS
        dimensions = ''
        product_finish = ''
        description = ''
        try:
            dimensions = info_wrap.find_element(By.CLASS_NAME, 'measurement-inch').get_attribute('innerHTML') + '\n'
        except:
            fails.append(product[0] + ' has no dimensions')
        try:
            product_finish = info_wrap.find_elements(By.TAG_NAME, 'p')[0].text + '\n'
        except:
            fails.append(product[0] + ' has no finish')
        try:
            desc_wrap = driver.find_element(By.CLASS_NAME, 'product-description')
            description = desc_wrap.find_elements(By.CLASS_NAME, 'additional-info')[0].text
        except:
            fails.append(product[0] + 'has no description')
        data.append( dimensions + product_finish + description )
        #images
        try:
            time.sleep(2)
            image_list = driver.find_elements(By.CLASS_NAME, 'fotorama__nav__frame--thumb')
            image_urls = []
            image_filenames = []
            c = 0
            if not image_list:
                image_urls.append( driver.find_element(By.CLASS_NAME, 'fotorama__loaded--img').get_attribute('href') )
            else:
                for pic in image_list:
                    if c != 0:
                        pic.click()
                        time.sleep(2)
                    image_urls.append( driver.find_element(By.CLASS_NAME, 'fotorama__active').get_attribute('href') )
                    c = c+1
            c = 1
            for pic in image_urls:
                file_name = sku + '-' + str(c)
                print(pic)
                urllib.request.urlretrieve(pic, 'Classic-Imports-and-Design/python webscrape/product-images/' + file_name + '.webp')
                image_filenames.append(file_name)
                c = c + 1
            try: 
                pic = driver.find_element(By.CLASS_NAME, 'dimensions-image').get_attribute('src')
                file_name = sku + '-' + str(c)
                urllib.request.urlretrieve(pic, 'Classic-Imports-and-Design/python webscrape/product-images/' + file_name + '.png')
                image_filenames.append(file_name)
            except:
                print('Standard Dimensions')
        except:
            fails.append(product[0] + ' FAILED TO GRAB IMAGES')
        
        pp(fails)
        data.append( ','.join(image_filenames) )
        print_table = data.copy()
        print_table[6] = 'desc...'
        print_table[7] = 'images...'
        print(tabulate([file_header] + [print_table]))
        print(data[6])
        print(data[7] + '\n')
        output_file.writerow(data)
    except:
        fails.append(product[0] + ' FAILED DUE TO UNKNOWN ERROR')
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
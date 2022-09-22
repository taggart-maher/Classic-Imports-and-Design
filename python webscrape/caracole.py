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
    #Name
    try:
        product_name = driver.find_elements(By.XPATH, '/html/body/div[1]/div[2]/div/div/div[1]/div/div[3]/div/div[2]/div/div[1]/h2[2]')[0].text 
        if product_name[0] == '*':
            product_name = product_name.lstrip('* ')
        data.append(product_name)
    except:
        fails.append(product[0] + ' has no name')
        continue
    #Brand
    data.append('Caracole')
    #Catagories
    data.append(product[1])
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
    #Description
    try:
        divs = driver.find_elements(By.CLASS_NAME, 'productinfoheading')
        product_overview = divs[1].find_elements(By.TAG_NAME, 'h3')
        index = 0
        for element in product_overview:
            if 'OVERVIEW' in element.text:
                break
            else:
                index = index + 1
        product_desc = divs[1].find_elements(By.TAG_NAME, 'p')[index].text
        product_desc = product_desc.replace('?', "'")
        data.append(product_desc)
    except:
        data.append('NA')
        fails.append(product[0] + ' has no description')
    #Images
    image_boxes = driver.find_elements(By.CLASS_NAME, 'col-xs-8')
    try:
        c = 1
        img_filenames = []
        for element in image_boxes:
            #there are many col-xs-8 in HTML page. We only want ones for RGB image
            if 'RGB' in element.text:    
                #ELEMENT = IMAGE BOX
                image_name = element.find_elements(By.TAG_NAME, 'strong')[0].text
                #match img name and product name. if >60% match then it probably is a product image
                if fuzz.partial_ratio(image_name.lower(), product_name.lower()) > 60:
                    #find description of image, if RGB image then we download it
                    image_details = element.find_elements(By.TAG_NAME, 'p')
                    for line in image_details:
                        if 'RGB' in line.text:
                            use_image = True
                            break
                        else:
                            use_image = False
                    if use_image == True:
                        dl_menu = element.find_elements(By.TAG_NAME, 'span')[0]
                        dl_menu.click()
                        time.sleep(1.25)
                        dl_menu = driver.find_elements(By.ID, 'file-download-modal')[0]
                        image_url = dl_menu.find_elements(By.TAG_NAME, 'a')[0].get_attribute('href')
                        file_name = product[0] + '-' + str(c) + '.jpg'
                        print('Downloading image:   ' + image_name + ' :  As > ' + file_name)
                        urllib.request.urlretrieve(image_url, 'Classic-Imports-and-Design/python webscrape/product-images/' + file_name)
                        img_filenames.append(file_name)                    
                        driver.find_elements(By.CLASS_NAME, 'close')[0].click()
                        time.sleep(.3)
                        c = c+1
                        use_image = False
        data.append( ','.join(img_filenames) )
    except Exception as err:
        fails.append(product[0] + ' has no images: ' + str(err))
        continue
    #Dimensions
    try:
        index = 0
        for element in product_overview:
            if '(IN)' in element.text:
                product_dim = divs[1].find_elements(By.TAG_NAME, 'p')[index].text
                break
            else:
                index = index + 1
        #L, W, H
        #caracole has W, D, H
        data.append(product_dim)
    except:
        fails.append(product[0] + 'has no dimensions')
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
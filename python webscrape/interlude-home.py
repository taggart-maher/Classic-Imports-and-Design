from selenium import webdriver 
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import csv
import urllib.request
from lxml import html
import time
from selenium.webdriver.support.ui import WebDriverWait
from pprint import pprint as pp

scrape_file = 'Classic-Imports-and-Design/python webscrape/url-lists/interlude-sku.csv'
login_url = 'https://www.interludehome.com/'

with open(scrape_file) as f:
    reader = csv.reader(f, delimiter=',')
    scrape_file = list(reader)

writefile = open('Classic-Imports-and-Design\python webscrape\output.csv', 'w+', encoding='UTF8')
output_file = csv.writer(writefile, delimiter=",")

driver = webdriver.Chrome('Classic-Imports-and-Design\python webscrape\chromedriver.exe')
#login
driver.get(login_url)
print('regencyantiqmd@aol.com')
print('108Rudin!07')
print("Please log into the wholesale account.")
input()

data = ['sku', 'Name', 'Brand', 'Categories', 'Wholesale', 'Retail', 'Description', 'Images', 'Length', 'Width', 'Height']
output_file.writerow(data)
fails = []

for product in scrape_file:
    product[0] = product[0].strip()
    product[1] = product[1].strip()
    data = []
    driver.get('https://www.interludehome.com/default/catalogsearch/result/?q=' + product[0])
    time.sleep(2.5)
    try:
        item_search_result = driver.find_elements(By.XPATH, '/html/body/div[1]/main/div[2]/div/div[6]/div/div[2]/ol/li/div/div/strong/a')[0]
        item_search_result.click()
    except:
        fails.append(product[0] + ' - could not load product page.')
        print(product[0] + ' does not exist')
        continue
    #Product Page
    time.sleep(3)
    #SKU
    data.append(product[0])
    #Name
    try:
        product_name = driver.find_elements(By.CLASS_NAME, 'pro-name')[0].text
        data.append(product_name)
    except:
        fails.append([product[0] +  ' has no name.'])
        continue
    #Brand
    data.append('Interlude Home')
    #Category
    data.append(product[1])
    #Wholesale
    try:
        wholesale = driver.find_elements(By.CLASS_NAME, 'price')[0].text
        wholesale = wholesale.lstrip('$').replace(',','')
        data.append(wholesale)
    #Retail
        retail = round(float(wholesale)*2)
        data.append(retail)
    except:
        data.append('0')
        data.append('0')
        fails.append(product[0] + ' has no wholesale price : ' + product[1])

    #Description
    try:
        description = driver.find_elements(By.XPATH, '//*[@id="description"]/div[1]/div[1]')[0].text
        data.append(description)
    except:
        data.append(product_name)
        fails.append(product[0] + ' has no description!')
    #Images
    try:
        image_caro = driver.find_elements(By.CLASS_NAME, 'fotorama__nav__frame--thumb') 
        c = 1
        img_filenames = []
        for img in image_caro:
            img.click()
            time.sleep(1.5)
            try:
                image = driver.find_elements(By.CLASS_NAME, 'fotorama__active')[0].get_attribute('href')
            except:
                image = driver.frind_elements(By.XPATH, '//*[@id="maincontent"]/div[2]/div/div[3]/div[2]/div[2]/div[2]/div[1]/div[3]/div/img')[0].get_attribute('src')
            urllib.request.urlretrieve(image, "Classic-Imports-and-Design/python webscrape/product-images/" + product[0] + "-" + str(c) +".jpg")
            img_filenames.append(product[0] + '-' + str(c))
            c = c+1
        data.append(','.join(img_filenames))
    except:
        fails.append(product[0] + ' - cannot get images')
        continue
    #Dimensions
    try:
        dimensions = driver.find_elements(By.CLASS_NAME, 'prdimens')[0].text
        dimensions = dimensions.split('X')
        data.extend((' ',' ',' ')) #this way if there are only 2 dims listed, it doesnt fail the try 
        data.append(dimensions[2].strip())
        data.append(dimensions[1].strip())
        data.append(dimensions[0].strip())
    except:
        fails.append(product[0] + ' has no dimensions.')

    pp(data)
    output_file.writerow(data)

pp(fails)
writefile.close()
#driver.get(url)
#time.sleep()
#content = driver.page_source
#soup = BeautifulSoup(content, "html.parser")
#tree = html.fromstring(driver.page_source) 

#tree.xpath()[0].text (.text needed if end of xpath NOT /text)
#soup.find("TAG-TYPE", class_="CLASS-NAME").text

#urllib.request.urlretrieve(IMG-URL, FILENAME) 

#output_file.writerow(data)
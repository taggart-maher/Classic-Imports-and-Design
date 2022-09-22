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

data = ['sku', 'Name', 'Brand', 'Category', 'Wholesale', 'Retail', 'Description', 'Images', 'Length', 'Width', 'Height']
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
    #Name
    try:
        data.append(driver.find_elements(By.XPATH, '/html/body/div[1]/section[3]/div/div/div/div/div/ui-view/shopping-container/div/ui-view/shopping-one-up/div[1]/div[1]/h2')[0].text) 
    except:
        data.append('ERROR')
        fails.append(product[0] + ' has no name')
    #Brand
    data.append('John Richard')
    #Category
    data.append(product[1])
    #Wholesale
    try:
        data.append( driver.find_elements(By.XPATH, '/html/body/div[1]/section[3]/div/div/div/div/div/ui-view/shopping-container/div/ui-view/shopping-one-up/div[2]/div/div[2]/div/div/div[7]/p/span/span')[0].text.lstrip('$').replace(',',''))
    #Retail
        data.append( round(float(data[4])*2.5) )
    except:
        data.append('ERROR')
        data.append('ERROR')
        fails.append(product[0] + ' has no wholesale')
    #Description
    try:
        data.append( driver.find_elements(By.XPATH, '/html/body/div[1]/section[3]/div/div/div/div/div/ui-view/shopping-container/div/ui-view/shopping-one-up/div[2]/div/div[2]/div/div/div[8]/div/div/p')[0].text ) 
    except:
        data.append('  ')
        fails.append(product[0] + ' has no description')
    #Images
    img_filenames = []
    c = 1
    while c < 20:
        img_url = "https://s3.amazonaws.com/emuncloud-staticassets/productImages/jr045/large/" + product[0] + ("" if c==1 else "_") + ("" if c==1 else str(c))
        img_url = img_url + ".jpg"
        try:
            urllib.request.urlretrieve(img_url, "Classic-Imports-and-Design/python webscrape/product-images/" + product[0] + "-" + str(c)+".jpg")
            img_filenames.append(product[0] + "-" + str(c))
            c = c+1
        except:
            #continue to nextimg
            c = c+1
    data.append(",".join(img_filenames))
    #Dimensions
    try:
        dimension_string = driver.find_elements(By.XPATH, '/html/body/div[1]/section[3]/div/div/div/div/div/ui-view/shopping-container/div/ui-view/shopping-one-up/div[2]/div/div[2]/shopping-one-up-heading/div[2]/div[1]/p[2]')[0].text
        dimension_list = dimension_string.split('X')
        data.append(dimension_list[2].strip())
        data.append(dimension_list[1].strip())
        data.append(dimension_list[0].strip())
    except:
        fails.append(product[0] + ' has no dimensions')
    pp(data)

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
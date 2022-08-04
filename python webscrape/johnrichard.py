from selenium import webdriver 
from bs4 import BeautifulSoup
import pandas as pd
import csv
import urllib.request
from lxml import html
import time

scrape_urls = r"Classic-Imports-and-Design\python webscrape\url-lists\johnrichard-urls.csv"
print('Name of Output CSV File')
filename = input()

file = open(filename+'.csv', 'w')
file.truncate()
writer = csv.writer(file)

driver = webdriver.Chrome("Classic-Imports-and-Design\python webscrape\chromedriver.exe")

#login
driver.get('https://www.johnrichard.com')
print("Please log into the wholesale account.")
input()

with open(scrape_urls) as f:
    reader = csv.reader(f)
    scrape_urls = list(reader)

for product in scrape_urls:
    print(product[0])
    #print(product[1])
    row = 1
    data = []
    print("Establishing connection to > " + product[0])
    driver.get("https://www.johnrichard.com/shop/" + product[0].strip() + "?position=-1")
    time.sleep(3)
    content = driver.page_source
    soup = BeautifulSoup(content, "html.parser")
    tree = html.fromstring(driver.page_source) 

    print("Scraping Information...")
    #SKU
    sku = tree.xpath("/html/body/div[1]/section[3]/div/div/div/div/div/ui-view/shopping-container/div/ui-view/shopping-one-up/div[1]/div[2]/h5")[0].text
    data.append(sku)
    #Product Title
    data.append(soup.find("h2", class_="ng-binding").text)
    #Brand
    #data.append("John Richard")
    #Category
    #data.append(product[1])
    #Wholesale Price
    #data.append(tree.xpath("/html/body/div[1]/section[3]/div/div/div/div/div/ui-view/shopping-container/div/ui-view/shopping-one-up/div[2]/div[1]/div[2]/shopping-one-up-heading/div[2]/div[1]/p/span/span")[0].text.lstrip("$"))
    #Item Description
    #description = tree.xpath("/html/body/div[1]/section[3]/div/div/div/div/div/ui-view/shopping-container/div/ui-view/shopping-one-up/div[2]/div[1]/div[2]/shopping-one-up-heading/div[3]/div/div/p[2]/text()")[0]
    #data.append(description)
    #Dimensions
    #dimensions = tree.xpath("/html/body/div[1]/section[3]/div/div/div/div/div/ui-view/shopping-container/div/ui-view/shopping-one-up/div[2]/div[1]/div[2]/div/shopping-one-up-details/product-more-info/panel/div/div/div/div/div[2]/product-dimensions/datum[1]/div/span[1]/span")[0].text
    #data.append(dimensions)

    #stock
    status = tree.xpath('/html/body/div[1]/section[3]/div/div/div/div/div/ui-view/shopping-container/div/ui-view/shopping-one-up/div[2]/div[1]/div[2]/div/shopping-one-up-details/product-more-info/div/product-availability/panel/div/div/div/div')[0].text

    #Images
    # print('Downloading product images...')
    # img_filenames = []
    # c = 1
    # while c < 20:
    #     img_url = "https://s3.amazonaws.com/emuncloud-staticassets/productImages/jr045/large/" + sku + ("" if c==1 else "_") + ("" if c==1 else str(c))
    #     img_url = img_url + ".jpg"
    #     try:
    #         urllib.request.urlretrieve(img_url, "product-images/" + sku + "-" + str(c)+".jpg")
    #         print(img_url)
    #         img_filenames.append(sku + "-" + str(c))
    #         c = c+1
    #     except:
    #         #continue to nextimg
    #         c = c+1
    # data.append(",".join(img_filenames))
    writer.writerow(data)
    print("Item " + sku + " written to CSV table.")

driver.close()



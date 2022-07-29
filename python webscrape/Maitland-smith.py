from selenium import webdriver 
from bs4 import BeautifulSoup
import pandas as pd
import csv
import urllib.request
from lxml import html
import time
from selenium.webdriver.support.ui import WebDriverWait
from pprint import pprint as pp

scrape_urls = "url-lists/maitland-urls.csv"
print('Name of Output CSV File')
filename = input()

file = open(filename+'.csv', 'w')
file.truncate()
writer = csv.writer(file)

driver = webdriver.Chrome("chromedriver.exe")

#login
driver.get('http://www.maitland-smith.com/')
print("Please log into the wholesale account.")
input()

with open(scrape_urls) as f:
    reader = csv.reader(f)
    scrape_urls = list(reader)

for product in scrape_urls:

    print(product[0])
    print(product[1])
    row = 1
    data = []
    print("Establishing connection to > " + product[0])
    try:
        driver.get("https://dealer.rockhousefarm.com/RHF/ShowItem/" + product[0].strip())
        time.sleep(3)
        content = driver.page_source
        soup = BeautifulSoup(content, "html.parser")
        tree = html.fromstring(driver.page_source) 
    except:
        print('ERROR!!!!!!! @46')
        continue

    print("Scraping Information...")
    #SKU
    sku_title = tree.xpath('/html/body/div[2]/div[5]/div[2]/h4[2]')[0].text.split(' - ')
    sku = product[0].strip()
    data.append(sku)
    #Title
    title = sku_title[1].strip()
    data.append(title)
    #Brand
    data.append('Maitland Smith')
    #Category
    data.append(product[1])
    #Wholesale Price
    driver.execute_script('var prices = ""')
    js = "$.post('/RHF/getPricingAndStock',{sku:'" + sku + "'}, function(data){$('#pricing').html(data);prices = data;})"
    driver.execute_script(js)
    time.sleep(3)
    try:
        wholesaleall = driver.execute_script('return prices')
        wholesalesoup = BeautifulSoup(wholesaleall, 'html.parser')
        wholesale = wholesalesoup.findAll('td')[3].text
        wholesale = wholesale.lstrip('$')
        data.append(wholesale)
        #Retail
        data.append(int(wholesale)*2)
    except:
        print("No price for item " + sku)
    #Item Description
    product_desc = driver.find_element('xpath', '/html/body/div[2]/div[5]/div[2]/div[2]').text
    data.append(title if product_desc == "Current Stock" else product_desc)
    #Item Dimensions
    w = soup.find('span', id='width').get_text()
    d = soup.find('span', id='depth').get_text()
    h = soup.find('span', id='height').get_text()
    data.append(w)
    data.append(d)
    data.append(h)
    #Images
    image_filenames = []
    images= soup.findAll('img', class_='img-responsive')
    imagelist = []
    for element in images:
        try:
            imagelist.append(element.get('src'))
        except:
            print('.')
    c = 0
    for element in imagelist:
        if 'prod-images' not in element:
            continue
        else:
            c = c+1
            img_url = "https://dealer.rockhousefarm.com" + element
            try:
                imgfile = sku + "-" + str(c) + ".jpg"
                urllib.request.urlretrieve(img_url, 'product-images/' + imgfile)
                image_filenames.append(imgfile.rstrip('.jpg'))
            except:
                print('.')
    pp('Images for Product # ' + sku)
    pp(image_filenames)
    data.append(",".join(image_filenames))
    pp(data)
    writer.writerow(data)
    print("Item " + sku + " written to CSV table.")
    
file.close()
driver.close()

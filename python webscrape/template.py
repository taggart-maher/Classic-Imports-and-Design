from selenium import webdriver 
from bs4 import BeautifulSoup
import pandas as pd
import csv
import urllib.request
from lxml import html
import time
from selenium.webdriver.support.ui import WebDriverWait
from pprint import pprint as pp

scrape_file
login_url

with open(scrape_file) as f:
    reader = csv.reader(f)
    scrape_urls = list(reader)

output_file = csv.writer( open('outputfile.csv', 'w').truncate() )


#login
driver.get(login_url)
print("Please log into the wholesale account.")
input()


#driver.get(url)
#time.sleep()
#content = driver.page_source
#soup = BeautifulSoup(content, "html.parser")
#tree = html.fromstring(driver.page_source) 

#tree.xpath()[0].text (.text needed if end of xpath NOT /text)
#soup.find("TAG-TYPE", class_="CLASS-NAME").text

#urllib.request.urlretrieve(IMG-URL, FILENAME) 

#output_file.writerow(data)
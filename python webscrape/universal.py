from selenium import webdriver 
from bs4 import BeautifulSoup
import pandas as pd
import csv
import urllib.request
from lxml import html
import time

scrape_urls = '\\url-lists\\list.csv'

output_file = 'output.csv'
output_file = open(output_file, 'w')
output_file.truncate()
output = csv.writer(output_file)

with open('parameters.csv', 'r') as input_file:
    input_reader = csv.Reader(input_file)
    line = 0
    for row in input_reader:
        if line==0:
            wholesale_login_url = row[1]
        if line==1:
            url_prefix = row[1]
        if line==2:
            url_suffix = row[1]
        


#login
driver.get('https://www.johnrichard.com')
print("Please log into the wholesale account.")
input()
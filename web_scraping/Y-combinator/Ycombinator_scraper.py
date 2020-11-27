#!/usr/bin/python3

from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import time
import re
import os


try:
    path = os.getenv('CHROMEDRIVER_HOME')
    driver = webdriver.Chrome(executable_path=path)
except Exception as e:
    driver = webdriver.Chrome(ChromeDriverManager().install())

url = 'https://www.ycombinator.com/companies'

driver.get(url)
time.sleep(10)

check_page_length = 0
try:
    # scroll to the end of the page
    while True:
        page_len = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        time.sleep(1)

        if check_page_length == page_len:
            break
            
        
        check_page_length = page_len
except:
    driver.close()



y_company_page_urls = []

# load selenium content to beautifulsoup
selenium_web_content = BeautifulSoup(driver.page_source, 'lxml')
get_company_list_block = selenium_web_content.body.find("div", attrs={"class":"SharedDirectory-module__section___1ljf9 SharedDirectory-module__results___3SG0w"})

a = 'https://www.ycombinator.com'
for company in get_company_list_block.find_all('a', href=True):

    y_link = company['href']                    # get the link to the company's page
    y_company_page_urls.append(a + y_link)

driver.close() # close selenium driver

print("Selenium closed, handing over to BeautifulSoup")

companies = []
count = 1
lenght = len(y_company_page_urls)
for url in y_company_page_urls:
    print(f"{count}/{lenght}")
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')

    section = soup.section 
    company_name = section.div.h1.text
    summary = section.div.p.text
    link = section.div.a.text


    box = section.find("div", attrs={'class':'highlight-box'})
    facts = box.find("div", attrs={'class':'facts'})

    info = []
    for fact in facts.find_all('div'):
        # founded, team size, location
        info.append(fact.span.text)

    company = {     "company_name": company_name,
                    "link" : link,
                    "summary" : summary,
                    "team_size" : info[1],
                    "founded" : info[0],
                    "location" : info[2]
            }

    companies.append(company)

    count += 1

# save the data scraped
path = "/home/dit/DiT/GitHub/Pylingo/Jupyters/Mr. Pipe work/ycombunator_data.csv"
df = pd.DataFrame(companies)
df.to_csv(path, index=False)
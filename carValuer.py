import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

os.environ['PATH'] += r'C:/Users/user/Desktop/seleniumDriver' 

base_url = ''
base_url = base_url[:-1]

# Add specific trim, optional
trim = 'R32'
if ' ' in trim:
    components = trim.split(' ')
    print(trim)
    trim = components[0] 
    for c in range(1, len(components)):
        trim += '%20' + components[c]
trim_url = f'&aggregatedTrim={trim}'
if len(trim) != 0:
    trim = trim_url

print(trim)

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
# options.add_experimental_option('detach', True)

driver = webdriver.Chrome(options=options)

time.sleep(3)

# li_class_name = "at__sc-1iwoe3s-2.iUeTOm"  
# advertisement_class_name = "span.at__sc-1n64n0d-11.at__sc-yv3gzn-3.jMmVJN.KruGO"  
# next_page_class_name = "a.at__sc-dyg8rq-0.chkuyu"  

hrefs = []

# Enter number of pages
n_pages = 12
n_pages = min(n_pages, 100)

try:
    for page in range(1, n_pages + 1):
        url = f'{base_url}{page}{trim}'
        driver.get(url)

        print(page)

        time.sleep(.5)

        # Wait for list items to be present
        wait = WebDriverWait(driver, 10)
        list_items = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'li.at__sc-1iwoe3s-2.iUeTOm')))

        # Filter list items based on absence of specific span element
        filtered_list_items = [li for li in list_items if not li.find_elements(By.CSS_SELECTOR, 'span.at__sc-1n64n0d-11.at__sc-yv3gzn-3.jMmVJN.KruGO')]

        # Extract hrefs from filtered list items
        for li in filtered_list_items:
            try:
                a = li.find_element(By.CSS_SELECTOR, 'a.at__sc-1n64n0d-7.at__sc-1mc7cl3-1.fcDnGr.fOXYeB')
                href = a.get_attribute('href')
                if href:
                    hrefs.append(href)
            except Exception as e:
                print(f"Exception occurred: {e}")
                    
finally:
    # Close the WebDriver
    driver.quit()

# Print or further process hrefs


for href in hrefs:
    print(href)

print(len(hrefs))

# Keep track of prices and mileages 
total_cars = len(hrefs)
total_price = 0
total_mileage = 0

driver = webdriver.Chrome(options=options)

print('Calculating value...')

try: 
    for href in hrefs:
        driver.get(href)

        if 'twcs=true' in href:
            time.sleep(0.1)

        time.sleep(0.1)

        wait = WebDriverWait(driver, 10)
        list_items = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'li.at__sc-1n64n0d-9.at__sc-1ebejir-1.hYdVyl.Gkuvm')))

        mileage_item = list_items[0]

        mileage_number_text = mileage_item.text.split(' ')[0]

        if ',' in mileage_number_text:
            mileage_number_separate = mileage_number_text.split(',')
            mileage = (int(mileage_number_separate[0]) * 1000) + int(mileage_number_separate[1])
        else:
            if not any(char.isdigit() for char in mileage_number_text):
                mileage = 1
            else:
                mileage = int(mileage_number_text)

        # print(mileage)

        total_mileage += mileage
        try:
            price_info = driver.find_element(By.CSS_SELECTOR, 'h2.at__sc-6sdn0z-6.kEwOIS')
        except Exception:
            try:
                price_info = driver.find_element(By.CSS_SELECTOR, 'h2.at__sc-6sdn0z-6.dEUZSI')
            except Exception:
                price_info = driver.find_element(By.CSS_SELECTOR, 'h2.at__sc-1n64n0d-2.kCqREX')
                print('Third option was triggered!')

        price_info_text = price_info.text[1:]
        print(price_info_text)
        print(href)
        if ',' in price_info_text:
            price_info_separate = price_info_text.split(',')
            price = (int(price_info_separate[0]) * 1000) + int(price_info_separate[1])
        else:
            price = int(price_info_text)

        # print(price)

        total_price += price

finally:
    
    driver.quit()


value = int(round((total_price/total_cars * total_mileage/total_cars) / 100000, 0))

print(f'The value of this car on Auto Trader is {value}')


    














import pandas as pd
import requests
from bs4 import BeautifulSoup
import json
import re, sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

def create_driver():
    opts = Options()
    opts.headless = True
    opts.add_argument("--headless=new")
    return webdriver.Firefox(options=opts)

# URL to scrape
exchanges = [
        {
            'name': 'gateio',
            'url': "https://www.gate.io/announcements/delisted"
        },
        {
            'name': 'bybit',
            'url': "https://announcements.bybit.com/en/?category=delistings"
        },
        {
            'name': 'binance',
            'url': "https://www.binance.com/en/support/announcement/list/161"
        }
    ]

# Make a GET request to fetch the raw HTML content
def fetch_gateio_delisted(url: str):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    article_list_container = soup.find('div', class_='article-list-box')
    
    if not article_list_container:
        return []

    delisted_dict = []
    for article_item in article_list_container.find_all('div', class_='article-list-item-content'):
        title = article_item.find('a').find('h3').find('span').text.strip()
        pairs = [p.strip() for p in re.findall(r'\((.*?)\)', title)]
        
        for pair in pairs:
            for token in pair.split(','):
                if token := token.strip():
                    delisted_dict.append({
                        'asset': token,
                        'symbol': f'{token}/USDT:USDT'
                    })

    return delisted_dict

def fetch_bybit_delisted(url: str):
    exchange = exchanges[1].get('name')
    url = exchanges[1].get('url')
    driver = None
    try:
        driver = create_driver()
        driver.get(url)
        content = driver.find_element(By.TAG_NAME, "body").text
        pattern = r"Delisting of \w+"
        matches = re.findall(pattern, content)
        delisted_dict = []
        for item in matches:
            pair = item.split(' ')[2].split('USDT')[0]
            symbol = pair + '/' + 'USDT' + ':USDT'
            result = {'asset': pair, 'symbol': f'{symbol}'}
            delisted_dict.append(result)

        return delisted_dict or []
    except Exception as e:
        print(f"Error in fetch_bybit_delisted: {e}")
        return []
    finally:
        if driver:
            driver.quit()

def fetch_binance_delisted(url: str):
    exchange = exchanges[2].get('name')
    url = exchanges[2].get('url')
    driver = None
    try:
        driver = create_driver()
        driver.get(url)
        content = driver.find_element(By.TAG_NAME, "body").text
        
        pattern = r"Binance Will Delist ([A-Za-z0-9, ]+?)(?:\son\s\d{4}|\s*$)"
        matches = re.findall(pattern, content)
        
        delisted_dict = []
        for match in matches:
            tokens = [token.strip() for token in match.split(',')]
            for token in tokens:
                if token:
                    result = {
                        'asset': token,
                        'symbol': f'{token}/USDT:USDT'
                    }
                    delisted_dict.append(result)
        
        return delisted_dict or []
    except Exception as e:
        print(f"Error fetching Binance delisted coins: {e}")
        return []
    finally:
        if driver:
            driver.quit()

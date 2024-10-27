import pandas as pd
import requests
from bs4 import BeautifulSoup
import json
import re
# URL to scrape
exchanges = [
        {
            'name': 'gateio',
            'url': "https://www.gate.io/announcements/delisted"
        },
        {
            'name': 'bybit',
            'url': "https://announcements.bybit.com/en/?category=delistings"
        }
    ]

# Make a GET request to fetch the raw HTML content
def fetch_delisted(url):
    exchange = exchanges[0].get('name')
    response = requests.get(url)
    print(response)
    if response.status_code == 200:
        print(f"{exchange} scheduled delisting!")
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        sys.exit('exit-requested!')

    # Parse the page content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the container with the announcements
    article_list_container = soup.find('div', class_='article-list-box')
    print()
    # Store extracted data
    announcements = []

    # Extract all individual announcement elements within the container
    for article_item in article_list_container.find_all('div', class_='article-list-item-content'):
        # Find the announcement title and link
        title_tag = article_item.find('a')
        title = title_tag.find('h3').find('span').text.strip() if title_tag else "No title found"
        #link = "https://www.gate.io" + title_tag['href'] if title_tag else "No link found"

        # Use regex to find any text in parentheses in the title
        parenthesis_text = re.findall(r'\((.*?)\)', title)  # This finds all text in parentheses

        # Append the extracted data to the list
        announcements.append({
            #'Title': title,
            #'Link': link,
            'Parenthesis Text': ', '.join(parenthesis_text)  # Join all matched texts if more than one
        })

    df = pd.DataFrame(announcements)
    #print(df.head())
    # Display the scraped announcements
    pairs = []
    for index, pair in enumerate(df['Parenthesis Text']):
        if pair:
            pairs.append(pair)
    delisted_dict = []
    for pair in pairs:
        result = {
            'asset': pair,
            'symbol': f'{pair}' + '/' + 'USDT' + ':USDT'
        }
        delisted_dict.append(result)

    return delisted_dict

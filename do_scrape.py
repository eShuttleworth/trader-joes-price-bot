import requests
from bs4 import BeautifulSoup

def scrape():
    url = 'https://traderjoesprices.com/'
    response = requests.get(url)
    webpage = response.content

    soup = BeautifulSoup(webpage, 'html.parser')
    table = soup.find('table')

    entries = []
    for row in table.find_all('tr')[1:]:  # Skipping the header row
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        entries.append(cols)

    return entries

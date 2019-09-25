# INFO
# Makes a request to https://coinmarketcap.com to get a page
# Grabs volume, price and circulating supply for top 1000 coins
# Collects the names and links of all coins and displays on excel
# Calculates approximate percentage of circulating supply being traded
#       activity = (volume / price) / circulating_supply

import requests
from bs4 import BeautifulSoup
from csv import writer


def req_page(url):
    page = requests.get(url)

    if not page.ok:  # Checks if server responds successfully
        print("Coin Market Cap server is down.")
    else:
        soup = BeautifulSoup(page.text, "html.parser")
    return soup


def get_data(soup):

    coins = soup.find('tbody').findAll('tr')

    for coin in coins:
        activity = 0
        name = coin.find(class_='currency-name-container link-secondary').get_text()
        rank = coin.find(class_='text-center').get_text()
        market_cap = coin.find(class_='no-wrap market-cap text-right').get_text()
        price = float(coin.find(class_='no-wrap text-right').get('data-sort'))
        volume = float(coin.find(class_='price').get('data-usd'))
        circulating_supply = float(coin.find(class_='no-wrap text-right circulating-supply').get('data-sort'))

        # Calculates activity
        activity = float((volume / price) / circulating_supply)

        print(rank, activity)


def main():
    url = 'https://coinmarketcap.com/'
    pages = 1
    while pages <= 10:
        url = ('https://coinmarketcap.com/') + str(pages)
        get_data(req_page(url))
        pages += 1


if __name__ == '__main__':
    main()


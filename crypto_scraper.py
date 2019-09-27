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

    coins = soup.find('tbody').findAll('tr', limit = 1000)

    with open('CryptoData.csv', 'w') as csv_file:
        csv_writer = writer(csv_file)
        headers = ['Rank', 'Coin', 'Market Cap', 'Price', 'Volume', 'Circulating Supply',
                   'Estimated Activity Percentage']
        csv_writer.writerow(headers)

        for coin in coins:
            rank = coin.find(class_='text-center').get_text()
            coin_name = coin.find(class_='currency-name-container link-secondary').get_text()
            market_cap = coin.find(class_='no-wrap market-cap text-right').get_text()
            price = float(coin.find(class_='no-wrap text-right').get('data-sort'))
            volume = float(coin.find(class_='price').get('data-usd'))
            circulating_supply = float(coin.find(class_='no-wrap text-right circulating-supply').get('data-sort'))

            # Calculates activity
            activity = float(format(((volume / price) / circulating_supply), '.15f'))
            activity_percentage = '{0:.12f}%'.format(activity * 100)

            csv_writer.writerow([rank, coin_name, market_cap, price, volume, circulating_supply,
                                 activity_percentage])


def main():
    url = "https://coinmarketcap.com/all/views/all/"
    get_data(req_page(url))


if __name__ == '__main__':
    main()


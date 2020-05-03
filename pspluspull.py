from bs4 import BeautifulSoup
import requests
from selenium import webdriver

headers = requests.utils.default_headers()
headers.update({'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'})

url = "https://www.playstation.com/en-us/explore/playstation-plus/"
req = requests.get(url, headers)
soup = BeautifulSoup(req.content, 'html.parser')

free_game_string = "PSPLUSFREEGAMES"

pulled_urls = []
for link in soup.find_all('a'):
    pulled_urls.append(link.get('href'))

clean_urls = [x for x in pulled_urls if x is not None]
free_game_urls = [i for i in clean_urls if free_game_string in i]

new_url = free_game_urls[0]
req = requests.get(new_url, headers)
soup = BeautifulSoup(req.content, 'html.parser')

new_pulled_urls = []
for link in soup.find_all('a'):
    new_pulled_urls.append(link.get('href'))

clean_pulled_urls = [x for x in new_pulled_urls if x is not None]
product_urls = [i for i in clean_pulled_urls if "/en-us/product/" in i]
products = list(set(product_urls))

store_prefix = "https://store.playstation.com"
product_urls = []
for item in products:
    product_urls.append(store_prefix + item)

driver = webdriver.Safari()
#driver.get("https://id.sonyentertainmentnetwork.com/signin/")

for item in product_urls:
    driver.execute_script("window.open('" + item + "');")
    driver.implicitly_wait(1)

driver.switch_to.window(driver.window_handles[1])
driver.close()

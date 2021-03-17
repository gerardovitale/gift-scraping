import json
from sys import path
from time import sleep

import requests
import selectorlib
from selectorlib import Extractor

from ScrapeAssistance.properties import PATH_DATA, PATH_HTML, PATH_YML
from ScrapeAssistance.ProxyGenerator import ProxyGenerator
from ScrapeAssistance.UserAgentGenerator import UserAgentGenerator


class ScrapeGift():

    def __init__(self, url:str):
        self.url = url[:url.find('?')]

    def get_header(self):
        return {
            'authority': 'www.amazon.com',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'dnt': '1',
            'upgrade-insecure-requests': '1',
            'user-agent': UserAgentGenerator().user_agent_random_choice(),
            'referrer': 'https://google.com',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'Pragma': 'no-cache',
        }

    def get_proxy(self):
        return {'https': ProxyGenerator().ip_random_choice()}

    def get_parameters(self):
        headers = self.get_header()
        proxy = self.get_proxy()
        selector = Extractor.from_yaml_file(PATH_YML)
        return {
            'headers': headers,
            'proxy': proxy,
            'selector': selector
        }

    def download_html(self, soup, path=PATH_HTML):
        with open(path, "w") as file:
            file.write(str(soup))
        print('[INFO] html downloaded')

    def download_data_as_json(self, data:selectorlib, path:str):
        with open(PATH_DATA + path, "w") as file:
            json.dump(data, file)
            file.write("\n")
        print('[INFO] data downloaded')

    def scrape_data_json(self, path:str):
        while True:
            parameters = self.get_parameters()
            try:
                html = requests.get(
                    self.url,
                    timeout=7,
                    headers=parameters['headers'],
                    proxies=parameters['proxy']
                )
                print(html)
                if html.status_code == 200:
                    print("[INFO] status: 200")
                    data = parameters['selector'].extract(html.text)
                    self.download_data_as_json(data, path=path)
                    return data
                print("[INFO] Sleeping...")
                sleep(5)
            except requests.exceptions.Timeout:
                print("[INFO] Timeout... Retrying connection")
                sleep(5)
                continue
            except requests.exceptions.ProxyError:
                print("[INFO] Proxy failed... Retrying connection")
                sleep(5)
                continue
            except requests.exceptions.SSLError:
                print("[INFO] SSL verification failed... Retrying connection")
                sleep(5)
                continue
            except requests.exceptions.HTTPError as error:
                raise SystemExit(error)

URL = "https://www.amazon.es/Cecotec-Aspirador-Rockstar-automático-Autonom%C3%ADa/dp/B08FDW7LCX/ref=sr_1_9?dchild=1&keywords=Dyson&qid=1615308855&sr=8-9&th=1"

amazon = ScrapeGift(URL)
amazon.scrape_data_json('test-4.json')

# <td class="a-span12">
# <span id="priceblock_ourprice" class="a-size-medium a-color-price priceBlockBuyingPriceString">249,00&nbsp;€</span>
# <span id="ourprice_shippingmessage">
# <span id="price-shipping-message" class="a-size-base a-color-base"></span>

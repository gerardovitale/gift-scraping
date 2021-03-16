import time
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import json
import re
from UserAgentGenerator import UserAgentGenerator
from ProxyGenerator import ProxyGenerator

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
        
    def get_soup(self):
        html = 0
        while html != 200:
            headers = self.get_header()
            print("[INFO] user-agent: ", headers['user-agent'])
            proxy = self.get_proxy()
            print("[INFO] proxy: ", proxy['https'])
            try:
                html = requests.get(self.url, timeout=7, headers=headers, proxies=proxy)
                print(html)
                print("[INFO] sleeping...")
                time.sleep(5)
            except:
                continue
        print("[INFO] Done! -> ", html)
        return BeautifulSoup(html.content, features="lxml")

        # title = soup.find(id='productTitle').get_text().strip()
        # try:
        #     price = float(soup.find(id='priceblock_ourprice').get_text().replace('.', '').replace('€', '').replace(',', '.').strip())
        # except:
        #     price = ''


URL = 'https://www.amazon.es/Cecotec-Aspirador-Rockstar-automático-Autonom%C3%ADa/dp/B08FDW7LCX/ref=sr_1_9?dchild=1&keywords=Dyson&qid=1615308855&sr=8-9&th=1'
cecotec_vacuum = ScrapeGift(URL)
print(cecotec_vacuum.get_soup())

# <td class="a-span12">
# <span id="priceblock_ourprice" class="a-size-medium a-color-price priceBlockBuyingPriceString">249,00&nbsp;€</span>
# <span id="ourprice_shippingmessage">
# <span id="price-shipping-message" class="a-size-base a-color-base"></span>
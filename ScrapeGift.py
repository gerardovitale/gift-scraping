import json
from time import sleep

import requests
from selectorlib import Extractor

from ScrapeAssistance.ProxyGenerator import ProxyGenerator
from ScrapeAssistance.UserAgentGenerator import UserAgentGenerator
from ScrapeAssistance.properties import PATH_DATA, PATH_HTML, PATH_YML


class ScrapeGift:

    def __init__(self, url: str):
        self.url = url[:url.find('?')]

    @staticmethod
    def _get_header():
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

    @staticmethod
    def _get_proxy():
        return {'https': ProxyGenerator().ip_random_choice()}

    def get_parameters(self):
        headers = self._get_header()
        proxy = self._get_proxy()
        selector = Extractor.from_yaml_file(PATH_YML)
        return {
            'headers': headers,
            'proxy': proxy,
            'selector': selector
        }

    @staticmethod
    def download_html(soup, path=PATH_HTML):
        with open(path, "w") as file:
            file.write(str(soup))
        print('[INFO] html downloaded')

    @staticmethod
    def download_data_as_json(data: Extractor, path: str):
        with open(PATH_DATA + path, "w") as file:
            json.dump(data, file)
            file.write("\n")
        print('[INFO] outputs downloaded')

    def scrape_data_json(self, path: str):
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


URL = "https://www.amazon.es/gp/product/B00SLE4KOO/ref=ox_sc_saved_title_6?smid=A1AT7YVPFBWXBL&psc=1"
ProxyGenerator().download_ip_as_txt()
amazon = ScrapeGift(URL)
amazon.scrape_data_json('test-6.json')
# "https://www.amazon.es/dp/B07TXCXRZ6/ref=cm_sw_r_sms_api_i_G1HX5ZDEJPZBEW084TDA"

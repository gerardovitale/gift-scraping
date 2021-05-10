from time import sleep

import requests
from selectorlib import Extractor

from ScrapeAssistance.DataManager import DataManager
from ScrapeAssistance.ProxyGenerator import ProxyGenerator
from ScrapeAssistance.UserAgentGenerator import UserAgentGenerator
from ScrapeAssistance.properties import PATH_YML


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

    def scrape_data_json(self, file_name: str):
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
                    DataManager().download_data_as_json(data, file_name=file_name)
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

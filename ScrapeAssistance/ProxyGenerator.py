from random import choice

import requests
from bs4 import BeautifulSoup

from ScrapeAssistance.properties import PATH_HTML, PATH_IP, URL_IP


class ProxyGenerator:

    def __init__(self, url=URL_IP):
        self.url = url[:url.find('?')]
        self.html = requests.get(url)
        self.soup = BeautifulSoup(self.html.content, features="lxml")

    def download_html(self, path: str):
        with open(PATH_HTML + path, "w") as file:
            file.write(str(self.soup))
        print('[INFO] html downloaded')

    def scrape_ip_list(self):
        soup = self.soup
        ip_list = map(lambda x: x.text, soup.findAll('td')[::8])
        port_list = map(lambda x: x.text, soup.findAll('td')[1::8])
        return list(map(
            lambda x: x[0] + ':' + x[1],
            list(zip(ip_list, port_list))
        ))[:300]
    
    def download_ip_as_txt(self, path=PATH_IP):
        ip_list = self.scrape_ip_list()
        with open(path, 'w') as file:
            for ip in ip_list:
                file.write("%s\n" % ip)
        print('[INFO] Proxy download completed')

    @staticmethod
    def ip_random_choice(path=PATH_IP):
        ip_list = open(path, 'r').readlines()
        return choice(ip_list).replace('\n', '')

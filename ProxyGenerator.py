import requests
from bs4 import BeautifulSoup
from random import choice

URL_IP = 'https://sslproxies.org/'
PATH_IP = 'resources/IP.txt'

class ProxyGenerator():

    def __init__(self, url=URL_IP):
        self.url = url[:url.find('?')]
        self.html = requests.get(url)
        self.soup = BeautifulSoup(self.html.text, features="lxml")

    def scrape_ip_list(self):
        soup = self.soup
        ip_list = map(lambda x:x.text, soup.findAll('td')[::8])
        port_list = map(lambda x:x.text, soup.findAll('td')[1::8])
        return list(map(
            lambda x:x[0] + ':' + x[1],
            list(zip(ip_list, port_list))
        ))[:100]
    
    def download_ip_list_as_txt(self, path=PATH_IP):
        ip_list = self.scrape_ip_list()
        with open(path, 'w') as file:
            for ip in ip_list:
                file.write("%s\n" % ip)
        return 'completed'
    
    def ip_random_choice(self, path=PATH_IP):
        ip_list = open(path, 'r').readlines()
        return choice(ip_list).replace('\n', '')
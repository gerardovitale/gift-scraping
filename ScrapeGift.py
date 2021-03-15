import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import json
import re
from UserAgent import UserAgent

headers = {
    'user-agent': UserAgent().user_agent_random_choice(),
    }

class ScrapeGift():

    def __init__(self, url:str):
        self.url = url[:url.find('?')]
        self.html = requests.get(url, headers=headers)
        self.soup = BeautifulSoup(self.html.text, features="lxml")

url = 'https://www.amazon.es/Cecotec-Aspirador-Rockstar-automático-Autonom%C3%ADa/dp/B08FDW7LCX/ref=sr_1_9?dchild=1&keywords=Dyson&qid=1615308855&sr=8-9&th=1'
cecotec_vacuum = ScrapeGift(url)
print(cecotec_vacuum.url)

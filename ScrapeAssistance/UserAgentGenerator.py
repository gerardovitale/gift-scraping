from random import choice
from ScrapeAssistance.properties import PATH_UA

class UserAgentGenerator():

    def __init__(self, path=PATH_UA):
        self.user_agent_list = open(path, 'r').readlines()
        self.len = len(self.user_agent_list)
    
    def user_agent_random_choice(self):
        return choice(self.user_agent_list).replace('\n', '')
from random import choice

UA_PATH = 'resources/UA.txt'

class UserAgent():

    def __init__(self, path=UA_PATH):
        self.user_agent_list = open(path, 'r').readlines()
        self.len = len(self.user_agent_list)
    
    def user_agent_random_choice(self):
        return choice(self.user_agent_list).replace('\n', '')

user_agent = UserAgent().user_agent_random_choice()
print(user_agent)
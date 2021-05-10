import json

from selectorlib import Extractor

from ScrapeAssistance.properties import PATH_DATA, PATH_HTML


class DataManager:
    def __init__(self):
        pass

    @staticmethod
    def download_html(soup, path=PATH_HTML):
        with open(path, "w") as file:
            file.write(str(soup))
        print('[INFO] html downloaded')

    @staticmethod
    def download_data_as_json(data: Extractor, file_name: str):
        with open(PATH_DATA + file_name, "w") as file:
            json.dump(data, file)
            file.write("\n")
        print('[INFO] outputs downloaded')

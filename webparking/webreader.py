# File name: webserver.py
"""
Read the content in webserver page
"""

import requests
import yaml


def read_web(address):
    """
    :param address: Address of the webserver
    :return: A dictonary with the parking informations
    """
    page = requests.get(address)
    if page.status_code == 200:  # Page downloaded succesfuly
        data = page.content.decode('utf-8')  # Converting page downloaded in bytes to str
        dic_data = yaml.load(data)  # Converting str to dict

        return dic_data  # Return a dict with parking informations

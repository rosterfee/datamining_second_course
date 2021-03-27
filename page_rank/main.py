import requests
import re

url = "https://stepik.org/catalog"

page = requests.get(url)
html = page.text

data = re.compile('https?://[\w.-]+')
links = data.findall(html)


def parse(dic: dict, url: str):

    counter = 0

    page = requests.get(url)
    html = page.text

    data = re.compile('https?://[\w.-]+')
    links = data.findall(html)
    for link in links:
      dic[url] = link;

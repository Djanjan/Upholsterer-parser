from scrapy.crawler import Crawler
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor
#from djan_parser.settings import SPIDER_LIFE_SECOND as max_parse_spider
#from djan_parser.settings import URL

import time
import sys
import requests
import json

process = CrawlerProcess(get_project_settings())
#"goodfonSpider","wallpaperscraftSpider", "oboitutSpider"
list_spider = ["goodfonSpider","wallpaperscraftSpider", "oboitutSpider"]

with open("items.json", 'w') as file:
        file.write("[")

for item in list_spider:
        process.crawl(item)

process.start()

with open("items.json", 'a') as file:
        file.write("{}]")

URL = 'http://localhost:8080/api/v1/image'

headers = {'Content-type': 'application/json',
           'Content-Encoding': 'utf-8'}

with open("items.json", "r") as write_file:
        js = json.load(write_file)
response = requests.post(URL, json=js, headers=headers)
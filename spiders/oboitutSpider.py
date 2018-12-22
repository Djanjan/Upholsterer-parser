# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from djan_parser.images import Image

from djan_parser.settings import max_count_items

class OboitutSpiderSpider(scrapy.Spider):
    name = 'oboitutSpider'
    allowed_domains = ['oboitut.com']
    settings = {}

    def start_requests(self):
        self.settings = {
            "Catalogs":{
                "city": "goroda",
                "games": "igry",
                "space":"kosmos",
                "animals":"podvodnyy-mir",
                "nature":"priroda",
                "fantasy":"fentezi"
            },
            "Count Images": 50
        }

        self.count_items = 0
        self.count_items_max = self.settings["Count Images"]
        yield scrapy.Request('https://oboitut.com/', self.parse)

    def parse(self, response):
        for imgConter in  response.css('div#dle-content div.verh'):
            img = imgConter.css('a::attr(href)').extract()
            catalog = imgConter.css('span.catcol a::attr(href)').extract_first()
            for key, value in self.settings["Catalogs"].items():
                if value == catalog.split("/")[3]:
                    yield scrapy.Request(img[1], callback=self.parse_image_page, 
                                        meta={'catalog': key})

        #Переход на следующию страницу
        hrefs = response.css('div.navigation a::attr(href)').extract()
        #href_page = response.urljoin(href)
        for href in hrefs:      
            yield response.follow(href, self.parse)

    def parse_image_page(self, response):
        image = response.css('div.news span.original a::attr(href)').extract_first()
        yield scrapy.Request(image, callback=self.parse_image, meta={'catalog': response.meta['catalog']})

    def parse_image(self, response):
        self.count_items += 1
        if (self.count_items >= self.count_items_max):
            raise scrapy.exceptions.CloseSpider(reason='Spider parsing -- END')

        yield {
            'url': response.url,
            'catalog': response.meta['catalog'],
        }

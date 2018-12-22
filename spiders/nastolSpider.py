# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from djan_parser.images import Image

from djan_parser.settings import max_count_items

class NastolSpider(scrapy.Spider):
    name = 'nastolSpider'
    allowed_domains = ['nastol.com.ua']
    settings = {}

    def start_requests(self):
        self.settings = {
            "Catalogs":{
                "girls":"girls"
            },
            "Count Images": 50
        }

        self.count_items = 0
        self.count_items_max = self.settings["Count Images"]
        yield scrapy.Request('https://www.nastol.com.ua/tags/%F1%E5%EA%F1%E8/', self.parse)

    def parse(self, response):
        for imgConter in  response.css('div#dle-content div.verh'):
            img = imgConter.css('a::attr(href)').extract()
            yield scrapy.Request(img[0], callback=self.parse_image_page)

        #Переход на следующию страницу
        hrefs = response.css('span.nav-center a::attr(href)').extract()
        for href in hrefs:      
            yield response.follow(href, self.parse)

    def parse_image_page(self, response):
        image = response.css('span.orig div a::attr(href)').extract_first()
        image_page = response.urljoin(image)

        self.count_items += 1
        if (self.count_items >= self.count_items_max):
            raise scrapy.exceptions.CloseSpider(reason='Spider parsing -- END')

        yield {
            'url': image_page,
            'catalog': "girls",
        }


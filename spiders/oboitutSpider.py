# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from djan_parser.images import Image

from djan_parser.settings import max_count_items

class OboitutSpiderSpider(scrapy.Spider):
    name = 'oboitutSpider'
    allowed_domains = ['oboitut.com']
    
    buff_catalog = str(" ")

    def start_requests(self):
        self.count_items = 0
        self.count_items_max = max_count_items
        yield scrapy.Request('https://oboitut.com/', self.parse)

    def parse(self, response):
        for imgConter in  response.css('div#dle-content div.verh'):
            img = imgConter.css('a::attr(href)').extract()
            catalog = imgConter.css('span.catcol a::attr(href)').extract_first()
            yield scrapy.Request(img[1], callback=self.parse_image_page, 
                                        meta={'catalog': catalog.split("/")[3]})

        #Переход на следующию страницу
        href = response.css('div.navigation a::attr(href)').extract_first()
        #href_page = response.urljoin(href)
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

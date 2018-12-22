# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from djan_parser.images import Image

from djan_parser.settings import max_count_items

class GoodfonspiderSpider(scrapy.Spider):
    name = 'goodfonSpider'
    allowed_domains = ['goodfon.ru']
    settings = {}
    
    buff_catalog = str(" ")

    def start_requests(self):
        self.settings = {
            "Catalogs":{
                "abstraction": "abstract",
                "city":"city",
                "animals":"animals",
                "games":"games",
                "space":"space",
                "macro":"macro",
                "minimalism":"minimalism",
                "music":"music",
                "nature":"nature",
                "textures":"textures",
                "hi-tech":"hi-tech",
                "fantasy":"fantasy",
                "rendering":"rendering"
            },
            "Count Images": 100
        }
        self.count_items = 0
        self.count_items_max = self.settings["Count Images"]
        yield scrapy.Request('http://goodfon.ru/', self.parse)

    def parse(self, response):
        for imgConter in response.css('div.wallpapers div.wallpapers__item'):
            img = imgConter.css('div.wallpapers__item__wall a::attr(href)').extract()
            image_page = response.urljoin(img[0])
            yield scrapy.Request(image_page, callback=self.parse_image_page)
                               # meta={'catalog': img[1].split("/")[4]})

        #Переход на следующию страницу
        href = response.css('div.paginator div.paginator__block div.paginator__block__bg a::attr(href)').extract_first()
        #href_page = response.urljoin(href)
        yield response.follow(href, self.parse)

    def parse_image_page(self, response):
        image = response.urljoin(response.css('div.wallpaper__item div.wallpaper__item__fon div.wallpaper__bottom div.wallpaper__download div a#download::attr(href)').extract_first())
        catal = response.css('div.wallpaper div.wallpaper__first div.wallpaper__catalog h2.wallpaper__zagh2 a::attr(href)').extract_first()

        for key, value in self.settings["Catalogs"].items():
                if value == catal.split("/")[4]:
                    yield scrapy.Request(image, callback=self.parse_image,
                                        meta={'catalog': key})


    def parse_image(self, response):
        self.count_items += 1
        if (self.count_items >= self.count_items_max):
            raise scrapy.exceptions.CloseSpider(reason='Spider parsing -- END')

        yield {
            'url': response.css('div.download div.download__second div.text_center a#im img::attr(src)').extract_first(),
            'catalog': response.meta['catalog'],
        }

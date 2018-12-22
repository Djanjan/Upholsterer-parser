# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from djan_parser.images import Image

from djan_parser.settings import max_count_items

class WallpaperscraftSpider(scrapy.Spider):
    name = 'wallpaperscraftSpider'
    allowed_domains = ['wallpaperscraft.ru']
    settings = {}

    def start_requests(self):
        self.settings = {
            "Catalogs":{
                "abstract": "abstract",
                "art":"art",
                "vector":"vector",
                "city":"city",
                "animals":"animals",
                "games":"games",
                "space":"space",
                "macro":"macro",
                "cars":"cars",
                "minimalism":"minimalism",
                "music":"music",
                "nature":"nature",
                "textures":"textures",
                "hi-tech":"hi-tech",
                "fantasy":"fantasy"
            },
            "Count Images": 100
        }
        self.count_items = 0
        self.count_items_max = self.settings["Count Images"]
        yield scrapy.Request('https://wallpaperscraft.ru/', self.parse)
 

    def parse(self, response):
        for imgConter in response.css('ul.wallpapers__list li.wallpapers__item'):
            img = imgConter.css('a::attr(href)').extract()
            image_page = response.urljoin(img[0])
            yield scrapy.Request(image_page, callback=self.parse_image_page)
                               # meta={'catalog': img[1].split("/")[4]})

        #Переход на следующию страницу
        hrefs = response.css('div.pager ul.pager__list li.pager__item a::attr(href)').extract()
        #href_page = response.urljoin(href)
        for href in hrefs:      
            yield response.follow(href, self.parse)

    def parse_image_page(self, response):
        image = response.urljoin(response.css('div.l-wrapper div.l-body div.l-layout.l-layout_tight div.content.content_wp.gui-row div.content-main div.wallpaper div.gui-row div.wallpaper-table span.wallpaper-table__cell a::attr(href)').extract_first())
        #catal = response.css('div.wallpaper div.wallpaper__first div.wallpaper__catalog h2.wallpaper__zagh2 a::attr(href)').extract_first()
        yield scrapy.Request(image, callback=self.parse_image)
                            #meta={'catalog': catal.split("/")[4]})

    def parse_image(self, response):
        catalog = response.css('div.l-body div.filters ul.filters__list.JS-Filters li.filter.filter_selected a::attr(href)').extract_first().split("/")[2]
        
        for key, value in self.settings["Catalogs"].items():
                if value == catalog:
                    self.count_items += 1
                    if (self.count_items >= self.count_items_max):
                        raise scrapy.exceptions.CloseSpider(reason="Spider "+self.name+' parsing -- END')

                    yield {
                        'url': response.css('body div.l-wrapper div.l-layout.l-layout_tight div.content-main div.wallpaper__placeholder img.wallpaper__image::attr(src)').extract_first(),
                        'catalog': key,
                    }



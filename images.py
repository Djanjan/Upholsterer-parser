# -*- coding: utf-8 -*-

import scrapy

class Image(scrapy.Item):
    url = scrapy.Field()
    catalog = scrapy.Field()
    last_updated = scrapy.Field(serializer=str)
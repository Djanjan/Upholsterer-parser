# -*- coding: utf-8 -*-
import json
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class DjanParserPipeline(object):
    def open_spider(self, spider):
        self.file_path = "items.json"
        self.file = open(self.file_path, 'a')
        #self.file.write("[")

    def close_spider(self, spider):
        self.file.close()
        #with open(self.file_path, 'a') as file:
        #   file.write("{}]")

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "," +"\n"
        self.file.write(line)
        return item

    #def process_item(self, item, spider):
    #   return item

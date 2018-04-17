# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json


class AppPipeline(object):
    def process_item(self, item, spider):
        return item


class JsonWriterPipeline(object):

    def __init__(self):
        self.file = open('items.json', 'a')

    def process_item(self, item, spider):
        print(str(spider))
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item

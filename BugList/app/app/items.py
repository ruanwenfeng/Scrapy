# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AppItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class DmozItem(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()
    desc = scrapy.Field()


# id
# desc
# assigned
# reporter
# cc
# version
# platform
# sys
# dependson
# blocked
# link
# creation_ts
# modified
# commname
# difflink
# newdiff
# filename
class BugItem(scrapy.Item):
    id = scrapy.Field()
    desc = scrapy.Field()
    assigned = scrapy.Field()
    reporter = scrapy.Field()
    dependson = scrapy.Field()
    blocked = scrapy.Field()
    duplicates = scrapy.Field()

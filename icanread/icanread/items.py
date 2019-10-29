# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class IcanreadItem(scrapy.Item):
    # define the fields for your item here like:
    character = scrapy.Field()
    level = scrapy.Field()
    title = scrapy.Field()
    image = scrapy.Field()
    format = scrapy.Field()

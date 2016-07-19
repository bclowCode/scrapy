# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MyprojectItem(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()
    image_urls = scrapy.Field()
    imgLink = scrapy.Field()
    desc = scrapy.Field()
    referral = scrapy.Field()


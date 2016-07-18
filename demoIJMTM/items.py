# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field
import scrapy


class DemoijmtmItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    URL=Field()
    title=Field()
    authortext=Field()
    authors=Field()
    journal=Field()
    date=Field()
    keytext=Field()
    neoKeytexts=Field()
    keywords=Field()
    count=Field()


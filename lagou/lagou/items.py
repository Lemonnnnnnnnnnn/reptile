# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LagouItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    city = scrapy.Field()
    companySize = scrapy.Field()
    education = scrapy.Field()
    skillLables = scrapy.Field()
    workYear = scrapy.Field()
    salary = scrapy.Field()
    companyShortName = scrapy.Field()

# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class VideoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class DouyinItem(scrapy.Item):
    title = scrapy.Field()
    rank_no = scrapy.Field()
    hot_value = scrapy.Field()
    video_url = scrapy.Field()


# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MovieSpider(scrapy.Item):
    rank_no = scrapy.Field()  # 排名
    img_url = scrapy.Field()  # 封面
    title = scrapy.Field()  # 标题
    star_num = scrapy.Field()  # 评分
    director = scrapy.Field()  # 导演
    main_role = scrapy.Field()  # 主演
    type = scrapy.Field()  # 电影类型
    nation = scrapy.Field()  # 国家
    language = scrapy.Field()  # 语言
    release_date = scrapy.Field()  # 上映日期
    length = scrapy.Field()  # 电影长度
    alternate_name = scrapy.Field()  # 又名，曾用名
    summary = scrapy.Field()  # 简述
    summary_url = scrapy.Field()  # 简述视频链接
    data_source = scrapy.Field() #数据源 1.豆瓣top250 21.IMDb_moive top250 22. IMDb_tv top250 3.烂番茄 4.metacritic
    rank_type = scrapy.Field() #排名类型

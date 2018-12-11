# -*- coding: utf-8 -*-
from functools import reduce

import scrapy
from ..items import MovieItem


def parse_detail(response):
    item = MovieItem()
    text_xpath = "//*[@id='info']/text()"  # 获取不带标签的文字
    text = [element.strip().encode('utf-8') for element in response.xpath(text_xpath).extract()]
    while "" in text:
        text.remove("")
    while "/" in text:
        text.remove("/")
    if len(text) > 3 and text[2].find("分钟"):
        text[2] = text[3]

    print(text)

    item["rank_no"] = "".join(response.xpath("//*[@id='content']/div[1]/span[1]/text()").extract()).replace("No.", "")  # 排名
    item["img_url"] = response.xpath("//div[@id='mainpic']/a[@class='nbgnbg']/img/@src").extract()  # 封面
    item["title"] = response.xpath("//div[@id='content']/h1/span[1]/text()").extract()  # 标题
    item["star_num"] = response.xpath("//strong[@class='ll rating_num']/text()").extract()  # 评分
    item["director"] = response.xpath("//div[@id='info']/span[1]/span[@class='attrs']/a/text()").extract()  # 导演
    item["main_role"] = " / ".join(response.xpath("//*[@id='info']/span[3]/span[@class='attrs']/a/text()").extract())  # 主演
    item["type"] = " / ".join(response.xpath("//*[@id='info']/span[@property='v:genre']/text()").extract())  # 电影类型
    item["nation"] = text[0]  # 国家
    item["language"] = text[1]  # 语言
    item["release_date"] = response.xpath("//div[@id='info']/span[@property='v:initialReleaseDate'][1]/text()").extract()  # 上映日期
    item["length"] = response.xpath("//*[@id='info']/span[@property='v:runtime']/text()").extract()  # 电影长度
    item["alternate_name"] = "".join(text[2])  # 又名，曾用名
    item["summary"] = "".join(response.xpath("//span[@property='v:summary']/text()").extract()).replace(" ", "").replace("\u3000", "")  # 简述
    item["data_source"] = 1
    print(item)


class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['movie.douban.com']
    start_urls = []

    for rankNo in range(1):
        if rankNo == 0:
            start_urls.append("https://movie.douban.com/top250")
        else:
            url = "https://movie.douban.com/top250?start=%d" % (rankNo * 25)
            start_urls.append(url)
    print(start_urls)

    def parse(self, response):
        detail_urls = response.xpath("//div[@class='hd']/a/@href")
        for url in detail_urls:
            yield scrapy.Request(url=url.extract(), callback=parse_detail, meta={})

# -*- coding: utf-8 -*-
import scrapy
from ..items import MovieSpider
from ..common import Common


def parse_list(response):
    rank_type = response.meta['rank_type']

    detail_urls = list(map(lambda x: "https://www.rottentomatoes.com"+x, response.xpath("//tr/td[3]/a[@class='unstyled articleLink']/@href").extract()))
    titleAndReleaseDate = list(map(lambda x: x.replace("/n", "").strip(),response.xpath("//tr/td[3]/a[@class='unstyled articleLink']/text()").extract()))

    for n in range(len(detail_urls)):
        item = MovieSpider()
        item["rank_type"] = rank_type
        item["rank_no"] = n + 1
        item["title"] = titleAndReleaseDate[n][0: -6].strip()
        item["release_date"] = titleAndReleaseDate[n][-5: -1]
        yield scrapy.Request(url=detail_urls[n],
                             callback=parse_detail,
                             meta={"data": item})


def parse_detail(response):
    item = response.meta['data']

    imgurl=''
    img_url1 = response.xpath("//div[@id='movie-image-section']/div//img/@src")
    img_url2 = response.xpath("//div[@id='movie-image-section']/div//img/@data-src")
    if len(img_url1) > 0:
        imgurl = img_url1[0].extract()
    elif len(img_url2) > 0:
        imgurl = img_url2[0].extract()

    if imgurl.startswith("/"):
        imgurl = "https://www.rottentomatoes.com"+imgurl

    item["img_url"] = imgurl
    item["star_num"] = response.xpath("//div[@id='all-critics-numbers']//span[@class='meter-value superPageFontColor']/span/text()").extract()[0]+"%"
    director = response.xpath(
        "//ul[@class='content-meta info']/li[@class='meta-row clearfix'][3]/div[@class='meta-value']/a/text()").extract()
    item["director"] = Common.judgeListAndJoinStr(director)
    roleList = response.xpath(
        "//div[@class='cast-item media inlineBlock ']/div[@class='media-body']/a[@class='unstyled articleLink']/span/text()").extract()
    item["main_role"] = Common.judgeListAndJoinStr(roleList)
    type = response.xpath("//ul[@class='content-meta info']/li[@class='meta-row clearfix'][2]/div[@class='meta-value']/a/text()").extract()
    item["type"] = Common.judgeListAndJoinStr(type)
    item["nation"] = ""
    item["language"] = ""
    lengths = response.xpath("//li[@class='meta-row clearfix']/div[@class='meta-label subtle']/text()").extract()
    length = ''
    for n in range(len(lengths)):
        if lengths[n].find("Runtime") >= 0:
            length = response.xpath("//li[@class='meta-row clearfix']["+str(n+1)+"]//time/text()").extract()[0]

    item["length"] = Common.clearBeforeAndAfterBlank(length)
    item["alternate_name"] = ""
    summary = response.xpath("//div[@id='movieSynopsis']/text()").extract()[0]
    item["summary"] = Common.clearBeforeAndAfterBlank(summary)
    item["summary_url"] = ""
    item["data_source"] = 3
    return item

# RottenTomatoesTop100 全排名类型
class RottenTomatoesTop100Spider(scrapy.Spider):
    name = 'rotten_tomatoes_top100'
    allowed_domains = ['www.rottentomatoes.com']
    start_urls = ['https://www.rottentomatoes.com/top/bestofrt/']

    def parse(self, response):
        type_name_list = list(map(lambda x: x.strip(), ["All Genres"] + response.xpath("//ul[@class='dropdown-menu']/li/a/text()").extract()))  # 类型列表
        urls = list(map(lambda x: "https://www.rottentomatoes.com" + x, response.xpath("//ul[@class='dropdown-menu']/li/a/@href").extract()))
        type_url_list = ['https://www.rottentomatoes.com/top/bestofrt/'] + urls

        #for n in range(1):
        for n in range(len(type_url_list)):
            rank_type = type_name_list[n]
            yield scrapy.Request(url=type_url_list[n],
                                 callback=parse_list,
                                 meta={"rank_type": rank_type})


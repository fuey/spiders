# -*- coding: utf-8 -*-
import scrapy
from ..items import MovieSpider
from ..common import Common


def parse_detail(response):
    item = response.meta['data']
    item["img_url"] = response.xpath("//div[@class='poster']/a/img/@src").extract()[0]
    item["title"] = response.xpath("//div[@class='title_wrapper']/h1/text()").extract()[0]
    item["star_num"] = response.xpath("//div[@class='ratingValue']/strong/span/text()").extract()[0]
    item["director"] = response.xpath("//div[@class='credit_summary_item'][1]/a/text()").extract()[0]
    item["main_role"] = " / ".join(response.xpath("//div[@class='credit_summary_item'][3]/a/text()").extract())


    type1 = response.xpath("//div[@class='subtext']/a[1]/@href").extract()[0]
    type2 = response.xpath("//div[@class='subtext']/a[2]/@href").extract()[0]

    type = ""
    if type1.find("title_type") > 0:
        type = response.xpath("//div[@class='subtext']/a[1]/text()").extract()[0]
    if type2.find("title_type") > 0:
        if len(type) > 0:
            type += " / " + response.xpath("//div[@class='subtext']/a[2]/text()").extract()[0]
        else:
            type = response.xpath("//div[@class='subtext']/a[2]/text()").extract()[0]
    item["type"] = type

    nation = response.xpath("//div[@id='titleDetails']/div[@class='txt-block'][1]/a/@href").extract()[0]
    if nation.find("country") > 0:  # 当没有官网地址时，第一个标签会是国家，第二个是语言
        nation = response.xpath("//div[@id='titleDetails']/div[@class='txt-block'][1]/a/text()").extract()
        item["nation"] = Common.judgeListAndJoinStr(nation)

        language = response.xpath("//div[@id='titleDetails']/div[@class='txt-block'][2]/a/text()").extract()
        item["language"]=Common.judgeListAndJoinStr(language)
    else:
        nation = response.xpath("//div[@id='titleDetails']/div[@class='txt-block'][2]/a/text()").extract()
        item["nation"] = Common.judgeListAndJoinStr(nation)

        language = response.xpath("//div[@id='titleDetails']/div[@class='txt-block'][3]/a/text()").extract()
        item["language"] = Common.judgeListAndJoinStr(language)

    item["release_date"] = response.xpath("//div[@class='subtext']/a[@title='See more release dates']/text()").extract()[0].replace("\n", "")

    length = response.xpath("//div[@class='subtext']/time/text()").extract()

    if len(length) > 0:
        item["length"] = "".join(response.xpath("//div[@class='subtext']/time/text()").extract()[0]).replace(" ", "").replace("\n", "")
    else:
        item["length"] = ""

    item["alternate_name"] = ''
    item["summary"] = "".join(response.xpath("//div[@class='summary_text']/text()").extract()[0]).replace("\n", "").strip()
    item["data_source"] = 22 #imdb_tv_top250
    return item
    #item["summary_url"] =response ""+response.xpath("//a[@class='slate_button prevent-ad-overlay video-modal']/@href").extract()[0]
    #summary_url = "https://www.imdb.com"+response.xpath("//a[@class='slate_button prevent-ad-overlay video-modal']/@href").extract()[0].replace("video/imdb","videoplayer")
    #yield scrapy.Request(url=summary_url, callback=parse_summary_url, meta={"data": item})


# def parse_summary_url(response):
#     item = response.meta['data']
#     item["summary_url"] = response.xpath("//video[@class='jw-video jw-reset']/@src").extract()[0]
#     return item


class ImdbTVTop250Spider(scrapy.Spider):
    name = 'imdb_tv_top250'
    allowed_domains = ['www.imdb.com']
    start_urls = ['https://www.imdb.com/chart/toptv']

    def parse(self, response):
        detail_urls = response.xpath("//tbody[@class='lister-list']/tr/td[@class='titleColumn']/a/@href").extract()
        #detail_urls = detail_urls[60:61]
        #title_info = response.xpath("//tbody[@class='lister-list']/tr/td[@class='titleColumn']")
        #rate_num = response.xpath("//tbody[@class='lister-list']/tr/td[@class='ratingColumn imdbRating']/strong")
        for n in range(len(detail_urls)):
            item = MovieSpider()
            item["rank_no"] = n+1
            yield scrapy.Request(url="https://www.imdb.com"+detail_urls[n],
                                 callback=parse_detail,
                                 meta={"data": item})

# -*- coding: utf-8 -*-
import scrapy
from ..items import MovieSpider
from ..common import Common


def parse_list(response):
    detail_url_list = response.xpath("//tr/td[@class='clamp-summary-wrap']/a[@class='title']/@href").extract()
    img_url_list = response.xpath("//tr/td[@class='clamp-image-wrap']/a[1]/img/@src").extract()
    title_list = response.xpath("//tr/td[@class='clamp-summary-wrap']/a[@class='title']/h3/text()").extract()
    rank_nos = response.xpath("//tr/td[@class='clamp-summary-wrap']/span[@class='title']/text()").extract()
    rank_no_list = Common.respace(rank_nos, ".", "")

    for n in range(len(detail_url_list)):
        item = MovieSpider()
        item["rank_no"] = rank_no_list[n]
        item["title"] = title_list[n]
        item["img_url"] = img_url_list[n]
        yield scrapy.Request(url="https://www.metacritic.com"+detail_url_list[n]+"/details",
                             callback=parse_detail_info,
                             meta={"data": item})


def parse_detail_info(response):
    item = response.meta['data']
    item["star_num"] = response.xpath("//tr/td[@class='left inset_right2']//a[@class='metascore_anchor']/span/text()").extract()[0]
    directors = response.xpath("//table[@class='credits'][1]/tbody/tr/td[@class='person']/a/text()").extract()
    item["director"] = Common.judgeListAndJoinStr(directors)
    main_roles = response.xpath("//table[@class='credits'][3]/tbody/tr/td[@class='person']/a/text()").extract()
    item["main_role"] = Common.judgeListAndJoinStr(main_roles)
    types = response.xpath("//tr[@class='genres']/td[@class='data']/span/text()").extract()
    item["type"] = Common.judgeListAndJoinStr(types)
    nations = response.xpath("//tr[@class='countries']/td/span/text()").extract()
    item["nation"] = Common.judgeListAndJoinStr(nations)
    languages = response.xpath("//tr[@class='languages']/td/span/text()").extract()
    item["language"] = Common.judgeListAndJoinStr(languages)
    item["release_date"] = response.xpath("//span[@class='release_date']/span[2]/text()").extract()[0]
    item["length"] = response.xpath("//tr[@class='runtime']/td[@class='data']/text()").extract()[0]
    item["alternate_name"] = ''
    item["summary"] = response.xpath("//div[@class='summary']/span[2]/text()").extract()[0]
    item["summary_url"] = ''
    item["data_source"] = 4
    item["rank_type"] = "ALL TIME"
    return item


class MtcAlltimeTopSpider(scrapy.Spider):
    name = 'mtc_alltime_top'
    allowed_domains = ['www.metacritic.com']
    start_urls = ['https://www.metacritic.com/browse/movies/score/metascore/all/filtered?sort=desc']

    def parse(self, response):
        max_page_num = response.xpath("//ul[@class='pages']/li[@class='page last_page']/a[@class='page_num']/text()").extract()[0]
        page_url_list = ["https://www.metacritic.com/browse/movies/score/metascore/all/filtered?sort=desc"]
        page_url_pre = "https://www.metacritic.com/browse/movies/score/metascore/all/filtered?sort=desc&page="

        # for page_no in range(int(max_page_num)+1):  # 这里+1的目的是为了让所有的链接都循环完毕
        for page_no in range(int(1)+1):
            if page_no != max_page_num:
                page_url_list.append(page_url_pre+str(page_no+1))
            yield scrapy.Request(url=page_url_list[page_no],  # 第0个链接（https://www.metacritic.com/browse/movies/score/metascore/all/filtered?sort=desc）开始的，所以上面必须得多循环一次才能跑完所有的链接
                                 callback=parse_list,
                                 meta={})

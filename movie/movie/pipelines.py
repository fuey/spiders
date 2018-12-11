# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql as pymysql
from scrapy import log

from scrapy.conf import settings


class MoviePipeline(object):
    def process_item(self, item, spider):

        pass
    # def __init__(self):
    #     # mysql
    #     self.connect = pymysql.connect(
    #         host=settings["MYSQL_HOST"],
    #         db=settings["MYSQL_DBNAME"],
    #         user=settings["MYSQL_USERNAME"],
    #         passwd=settings["MYSQL_PASSWORLD"],
    #         charset='utf8')
    #         #use_unicode=True)
    #
    #     # 通过cursor执行增删查改
    #     self.cursor = self.connect.cursor()
    #
    # def process_item(self, item, spider):
    #     try:
    #
    #         # 插入数据豆瓣top250
    #         sql = "insert into spider_movie( `rank_no`, `img_url`, `title`, `star_num`, `director`, `main_role`, `type`, `nation`, `language`, `release_date`, `length`, `alternate_name`, `summary`) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    #         self.cursor.execute(sql, (
    #             item["rank_no"], item["img_url"], item["title"], item["star_num"], item["director"], item["main_role"],
    #             item["type"], item["nation"], item["language"], item["release_date"], item["length"],
    #             item["alternate_name"], item["summary"]))
    #
    #         # 提交sql语句
    #         self.connect.commit()
    #
    #     except Exception as error:
    #         # 出现错误时打印错误日志
    #         log.msg(error)
    #     return item

# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from twisted.enterprise import adbapi
import pymysql
from scrapy import log
from scrapy.crawler import Settings as settings


def dbHandle():
    connect = pymysql.connect(
        user="root",
        password="root",  # 连接数据库，不会的可以看我之前写的连接数据库的文章
        port=3306,
        host="127.0.0.1",
        db="read-rank",
        charset="utf8"
    )
    return connect


class MoviespiderPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(host='127.0.0.1', user='root', passwd='root', db='read-rank', port=3306, charset="utf8")
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        # sql = "insert into douban_top250( `rank_no`, `img_url`, `title`, `star_num`, `director`, `main_role`, `type`, `nation`, `language`, `release_date`, `length`, `alternate_name`, `summary`) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        # self.cursor.execute(sql, ( item["rank_no"], item["img_url"], item["title"], item["star_num"], item["director"], item["main_role"],item["type"], item["nation"], item["language"], item["release_date"], item["length"],item["alternate_name"], item["summary"]))
        # self.conn.commit()

        # 插入数据豆瓣top250
        sql = "insert into spider_movie( `rank_no`, `img_url`, `title`, `star_num`, `director`, `main_role`, `type`, `nation`, `language`, `release_date`, `length`, `alternate_name`, `summary`, `data_source`, `rank_type`) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        try:
            self.cursor.execute(sql, (
                item["rank_no"], item["img_url"], item["title"], item["star_num"], item["director"],
                item["main_role"], item["type"], item["nation"], item["language"], item["release_date"],
                item["length"], item["alternate_name"], item["summary"], item["data_source"], item["rank_type"]))

            # 提交sql语句
            self.conn.commit()
        except Exception as error:
            log.msg(error)
        return item

        # return item
    def close_spider(self, spider):
        self.conn.close()

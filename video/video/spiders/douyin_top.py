# -*- coding: utf-8 -*-
import scrapy
import time
import json
import urllib.parse
import requests
import pymysql
import datetime
from scrapy import log

headers = {
    "Cookie": "install_id=53112482656; ttreq=1$a4ed279b42b9acb3dee9a3a3c2d645ce99ed786f; odin_tt=38d535495242f853ffdf693ae531a152910b1047bbb3ba5c8e2fa7f3cbd7f6a1ec9f6027fc44ea36c4bd45281487d4a7; sid_guard=d074b1c430eef87a3599e20ef34a5555%7C1543976393%7C5184000%7CSun%2C+03-Feb-2019+02%3A19%3A53+GMT; uid_tt=4e0b25bc326fae6b428afc5826243eeb; sid_tt=d074b1c430eef87a3599e20ef34a5555; sessionid=d074b1c430eef87a3599e20ef34a5555",
    "Accept-Encoding": "gzip",
    "X-SS-REQ-TICKET": "1543976807598",
    "X-Tt-Token": "00d074b1c430eef87a3599e20ef34a5555b97ecb95bff1a3d1a81726386a1adf7a91df6c32bfa121fc10400ffede8df72016",
    "sdk-version": "1",
    "X-SS-TC": "0",
    "User-Agent": "com.ss.android.ugc.aweme/350 (Linux; U; Android 8.0.0; zh_CN; MI 5; Build/OPR1.170623.032; Cronet/58.0.2991.0)"
}


def getVideo(key):
    '''
    获取第一个视频连接地址
    :param key:
    :return:
    '''
    # 编译关键词
    key = urllib.parse.quote(key)
    # 拼接关键词搜索接口url
    url = 'https://api.amemv.com/aweme/v1/general/search/single/?keyword=' + key + '&offset=0&count=10&is_pull_refresh=0&hot_search=0&latitude=30.725991&longitude=103.968091&ts=1543984658&js_sdk_version=1.2.2&app_type=normal&manifest_version_code=350&_rticket=1543984657736&ac=wifi&device_id=60155513971&iid=53112482656&os_version=8.0.0&channel=xiaomi&version_code=350&device_type=MI%205&language=zh&uuid=862258031596696&resolution=1080*1920&openudid=8aa8e21fca47053b&update_version_code=3502&app_name=aweme&version_name=3.5.0&os_api=26&device_brand=Xiaomi&ssmix=a&device_platform=android&dpi=480&aid=1128&as=a1e5055072614ce6a74033&cp=5813c65d2e7d0769e1[eIi&mas=01327dcd31044d72007555ed00c3de0b5dcccc0c2cec866ca6c62c'
    # 获取搜索界面并转化为json对象
    rsp = requests.post(url, headers=headers)
    postHTML = rsp.content.decode(rsp.apparent_encoding, 'ignore')
    jsonObj = json.loads(postHTML)
    # 获取data对应v
    metes = jsonObj['data']
    nums = len(metes)
    uri = ''
    # 多个视频列表捕获第一个视频地址即刻返回视频uri(视频唯一标识)
    for _ in range(nums):
        data = metes[_]['aweme_info']['video']
        if 'download_suffix_logo_addr' in data.keys():
            uri = data['download_suffix_logo_addr']['uri']
            break
    # 拼接视频地址
    videoURL = 'https://aweme.snssdk.com/aweme/v1/playwm/?video_id=' + uri + '&line=0'
    # 返回视频地址
    return videoURL


class DouyinTopSpider(scrapy.Spider):
    name = 'douyin_top'
    ts = str(time.time())
    # 入口url（热门列表url）
    start_url = 'https://aweme.snssdk.com/aweme/v1/hot/search/list/?detail_list=0&ts=' + ts + '&js_sdk_version=1.2.2&app_type=normal&manifest_version_code=350&_rticket=1543976807872&ac=wifi&device_id=60155513971&iid=53112482656&os_version=8.0.0&channel=xiaomi&version_code=350&device_type=MI%205&language=zh&resolution=1080*1920&openudid=8aa8e21fca47053b&update_version_code=3502&app_name=aweme&version_name=3.5.0&os_api=26&device_brand=Xiaomi&ssmix=a&device_platform=android&dpi=480&aid=1128&as=a1c56320b7f6ccc7874900&cp=3d63c15f7576037de1_uMy&mas=01258b5acd59f6bccb58178086286fdded0c0c9c2cec1cecc6c6c6'
    rsp = requests.get(start_url, headers=headers)
    html = rsp.content.decode(rsp.apparent_encoding, 'ignore')
    jsonObj = json.loads(html)
    word_list = jsonObj['data']['word_list']
    index = 1

    conn = pymysql.connect(host='127.0.0.1', user='root', passwd='root', db='read-rank', port=3306, charset="utf8")
    cursor = conn.cursor()

    # 循环解析每个热门事件

    try:
        for li in word_list:
            word = li['word']
            hot_value = li['hot_value']
            hot_index = index
            videoURL = getVideo(word)
            index += 1
            dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print("排名：%d ,标题: %s ,热度值: %d ,视频下载地址: %s" % (hot_index, word, hot_value, videoURL))
            sql = "INSERT INTO `read-rank`.`spider_video_douyin` ( `rank_no`, `video_url`, `title`, `hot_value`, `date_time`) VALUES ( %s, %s, %s, %s, %s)"
            cursor.execute(sql, (hot_index, videoURL, word, hot_value, dt))
            time.sleep(2)

    except Exception as e:
        print(e)
        log.msg(e)
    finally:
        conn.close()


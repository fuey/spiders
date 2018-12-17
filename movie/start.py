from scrapy import cmdline

cmdline.execute("scrapy crawl douban".split());
# cmdline.execute("scrapy crawl imdb_movie_top250".split())
# cmdline.execute("scrapy crawl imdb_tv_top250 -s LOG_FILE=spider.log".split())
# cmdline.execute("scrapy crawl rotten_tomatoes_top100".split())
# cmdline.execute("scrapy crawl mtc_alltime_top".split())

BOT_NAME = 'padcrawler'

SPIDER_MODULES = ['padcrawler.spiders']
NEWSPIDER_MODULE = 'padcrawler.spiders'


# USER_AGENT = 'padcrawler (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

DOWNLOAD_DELAY = 5

DOWNLOADER_MIDDLEWARES = {
    'padcrawler.middlewares.IgnoreDuplicatesMiddleware': 543,
}

ITEM_PIPELINES = {
    'padcrawler.pipelines.SQLStorePipeline': 300,
}

AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 5
AUTOTHROTTLE_MAX_DELAY = 60
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
AUTOTHROTTLE_DEBUG = False


# padcrawler settings

MAX_POST_AGE_DAYS = 14

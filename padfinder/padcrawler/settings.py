BOT_NAME = 'padcrawler'

SPIDER_MODULES = ['padcrawler.spiders']
NEWSPIDER_MODULE = 'padcrawler.spiders'


# USER_AGENT = 'padcrawler (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

DOWNLOAD_DELAY = 30
RANDOMIZE_DOWNLOAD_DELAY = True

DOWNLOADER_MIDDLEWARES = {
    'padcrawler.middlewares.IgnoreDuplicatesMiddleware': 543,
}

ITEM_PIPELINES = {
    'padcrawler.pipelines.SQLStorePipeline': 300,
}


# padcrawler settings

MAX_POST_AGE_DAYS = 14

# -*- coding: utf-8 -*-

# Scrapy settings for demoIJMTM project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'demoIJMTM'

SPIDER_MODULES = ['demoIJMTM.spiders']
NEWSPIDER_MODULE = 'demoIJMTM.spiders'

DOWNLOADER_MIDDLEWARES = {
    'demoIJMTM.middlewares.Headermiddleware': 551,
    'scrapy.downloadermiddlewares.defaultheaders.DefaultHeadersMiddleware': None,
}

ITEM_PIPELINES = {
    #'demoIJMTM.pipelines.singlejournal_Pipeline':300
    'demoIJMTM.pipelines.index_Pipeline':300,
    #'demoIJMTM.pipelines.ijmtmPipeline':301
    }

CONCURRENT_REQUESTS=1

RETRY_ENABLED=False

#HTTPERROR_ALLOW_ALL=True

#CONCURRENT_REQUESTS_PER_DOMAIN=1
#DOWNLOAD_DELAY = 1

#DEFAULT_REQUEST_HEADERS={
    #'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    #'Accept-Language': 'en',
#    'Accept': 'text/xml',
#    'X-ELS-APIKey':'a6e5b042c6e04a7d66e62a47427f8b73'
#}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'demoIJMTM (+http://www.yourdomain.com)'

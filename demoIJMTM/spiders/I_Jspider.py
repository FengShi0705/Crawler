import scrapy

from demoIJMTM.items import DemoijmtmItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import codecs
from scrapy.exceptions import CloseSpider
import time
from demoIJMTM.user_login import APIKey, Check_update_count
import SpdFun
from demoIJMTM.Save_Log import logfun
from datetime import date



class I_Jspider(CrawlSpider):
    name = 'Jspider'
    apiheader='b4273b1bd02ea3a124a1d25cdc2823cd'
    #count_limit = 400000
    #HTTPERROR_ALLOW_ALL=True
    #handle_httpstatus_all=True
    #date_count={"today":{"date":date.today(),"count":0},"lastday":{"date":date.today(),"count":0}}

    # filter to get English journals
    flt=SpdFun.EnJ()
    #already finished up_A,B,C,D,E,F,G,H,up_I,up_J,K,L,up_M,N,O,P,Q,R,S,T journals
    #processing U journals
    flt.Eng_jnl('http://api.elsevier.com/sitemap/page/sitemap/u.html')
    allowed_domains=['elsevier.com']

    #reject existing journals
    existing_journals = logfun.Reject_Exsting_Journals('total_v3_csvneo4j')
    start_urls=[n for n in flt.enitems if n not in existing_journals] #OK
    #existing_journals[:-1]

    ###start_urls=["http://api.elsevier.com/content/article/pii/S0014482714005539"]

    rules = (
        Rule(LinkExtractor(allow=flt.paper_urls),
             callback='parse_item', follow = True,),

        Rule(LinkExtractor(allow=flt.Jurls),#deny=rejjournals),
             callback='parse_volume', follow = True,),
        )


    def parse_item(self,response): # all information in item are output as utf-8

        #print header
        print response.request.headers['X-ELS-APIKey']

        #define item
        item=DemoijmtmItem()
        #count item
        self.state['items_count'] = self.state.get('items_count', 0) + 1
        item['count']=self.state['items_count']

        #check response status
        #--
        #if response.status in [400,401,403,429]:
        #    webdriverhead=APIKey()
        #    if webdriverhead.recursive_APIKey(self.name,self.apiheader,0)==0:
        #        raise CloseSpider('webdriver wrong in spider')
        #    else:
        #        self.apiheader=webdriverhead.newkey
        #        return item
        #--

        #check limit
        #if Check_update_count(self.date_count,item['count'], self.count_limit):
        #    raise CloseSpider("Exceed weekly limited (in spider)")
        #else:
        SpdFun.response2item(response,item)
        return item


    def parse_volume(self,response):
        #print header
        print response.request.headers['X-ELS-APIKey']

        #assign item
        item=DemoijmtmItem()
        #count item
        self.state['items_count'] = self.state.get('items_count', 0) + 1
        item['count']=self.state['items_count']

        #check response status
        #--
        #if response.status in [400, 401, 403, 429]:
        #    webdriverhead=APIKey()
        #    if webdriverhead.recursive_APIKey(self.name,self.apiheader,0)==0:
        #        raise CloseSpider('webdriver wrong in spider')
        #    else:
        #        self.apiheader=webdriverhead.newkey
        #        return item
        #--

        #check limit
        #if Check_update_count(self.date_count,item['count'],self.count_limit):
        #    raise CloseSpider("Exceed weekly limited (in spider)")
        #else:
        return item


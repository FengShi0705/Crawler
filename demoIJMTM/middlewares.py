
from user_login import APIKey
import time
import re

class Headermiddleware(object):
    def process_request(self,request,spider):

        print spider.state.get('items_count', 0)
        #too many request
        #--
        #if (spider.state.get('items_count', 0)>=10000) and (spider.state.get('items_count', 0)%19000==0):
        #    webdriverhead=APIKey()
        #    if webdriverhead.recursive_APIKey(spider.name,spider.apiheader,0)==0:
        #        print 'Webdriver wrong in middleware'
        #    else:
        #        spider.apiheader=webdriverhead.newkey
        #--

        #assign headers
        request.headers['Accept']='text/xml'
        request.headers['X-ELS-APIKey']=spider.apiheader
        #filter fields
        if re.search(r'content/article/pii/S',request.url):
            request._set_url(request.url+'?field=subject,coverDate,title,creator,publicationName')


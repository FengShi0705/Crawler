import urllib2
from lxml import html
import re
import mysql.connector
import nltk
import enchant
import string
from FengPrivate import functions
from scrapy.loader.processors import Join
from scrapy.selector import Selector


class EnJ:

# This function take in "site" which is the url of Index start url
# it generates a list of journal urls, regex journal urls and regex paper urls whose journal title only contains English words.
    def Eng_jnl(self,site):
        Dgb=enchant.Dict("en_GB")
        Dus=enchant.Dict("en_US")

        req = urllib2.Request(site)
        page = urllib2.urlopen(req)
        content=page.read()
        self.tree=html.fromstring(content)

        self.enitems=[]
        for i,url in enumerate(self.tree.xpath('//a/@href')):
            if re.search(r"sitemap/page/sitemap/serial/journals",url):
                try:
                    self.tree.xpath('//a/text()')[i].encode('ascii') # be ascii code
                except:
                    continue
                else:
                    words=nltk.word_tokenize(self.tree.xpath('//a/text()')[i])
                    sign=0
                    for word in words:
                        if Dgb.check(word) or Dus.check(word) or word in string.punctuation: # be English words or punctuation
                            continue
                        else:
                            sign=1
                    if sign==0:
                        self.enitems.append(url)

        self.paper_urls=[]
        for n in self.enitems:
            pu="content/article/pii/S"+n.split('/')[-1].split('.')[0]
            self.paper_urls.append(pu)

        self.Jurls=[m.split('.')[2][4:] for m in self.enitems]
        return

# This function take in "site" which is the url of Index start url
# it return a list of journal urls whose title only contains ascii character.
    def for_ascii(self,site):

        req = urllib2.Request(site)

        page = urllib2.urlopen(req)

        content=page.read()
        self.tree=html.fromstring(content)

        self.ascitems=[]


        for i,url in enumerate(self.tree.xpath('//a/@href')):
            if re.search(r"sitemap/page/sitemap/serial/journals",url):
                try:
                    self.tree.xpath('//a/text()')[i].encode('ascii')
                except:
                    continue
                else:
                    self.ascitems.append(url)


#get journal's number which have already been downloaded in a specific schema in mysql database
class F_exsiting_journals:

    def get_exsiting_journal_url(self,dbname):
        #dbname is schema for example "a_journals" or "j_journals" in mysql databases

        cnx = mysql.connector.connect(user='root',password='Lostyourface123',database=dbname)
        cursor = cnx.cursor()
        query="show tables"
        cursor.execute(query)
        tables=[]
        for i in cursor:
            tables.append(i[0].encode('utf-8'))

        whole=[]
        for n in tables:
            if re.search('_150723_whole',n):
                whole.append(n)

        self.j_num=[]
        for n in whole:
            query="select url from `{}` where id=1".format(n)
            cursor.execute(query)
            for i in cursor:
                self.j_num.append(i[0].encode('utf-8').split('pii/S')[1][0:8])


        for i,n in enumerate(self.j_num):
            self.j_num[i]="sitemap/page/sitemap/serial/journals/{}/".format(dbname.split('_')[0])+n

        #self.j_num is the list of existing journal number





        self.j_name=[] #list of journals' names already downloaded in that schema in mysql
        for i in xrange(0,400):
            self.j_name.append(' ')

        for n in whole:
            query="select `Journal` from `{}` where id=1".format(n)
            ind=int(n.split('_')[0])
            cursor.execute(query)
            for i in cursor:
                self.j_name[ind]=i[0].encode('utf-8')



        #journals number existing in the mysql by order

        self.jnum_ord=[]
        for i in xrange(0,400):
            self.jnum_ord.append(' ')

        for n in whole:
            query="select `URL` from `{}` where id=1".format(n)
            ind=int(n.split('_')[0])
            cursor.execute(query)
            for i in cursor:
                self.jnum_ord[ind]=i[0].encode('utf-8').split('pii/S')[1][0:8]

        for i,n in enumerate(self.jnum_ord):
            self.jnum_ord[i]="sitemap/page/sitemap/serial/journals/{}/".format(dbname.split('_')[0])+n



# With response status OK, process item.
# all information are output as utf-8
def response2item(response,item):
    sel=Selector(response)
    s_join=Join()
    c_join=Join(separator=u'<>')

    words=sel.xpath('//*[name()="dcterms:subject"]//text()').extract()
    date=sel.xpath('//*[name()="prism:coverDate"]//text()').extract()
    datejoin=s_join(date)
    year=datejoin.encode('utf-8').split('-')[0]

    if words==[] or int(year)<1995:
        return
    else:
        #URL
        item['URL']=response.url.split('?')[0] # utf-8 string
        #title
        topic=sel.xpath('//*[name()="dc:title"]//text()').extract()
        if topic==[]:
            title=''
        else:
            title=topic[0]
        item['title'] = title.strip().replace('\n','').replace('"',"'").replace(';','').encode('utf-8') # utf-8 string
        #author
        authors=sel.xpath('//*[name()="dc:creator"]//text()').extract()
        item['authortext']=c_join(authors).encode('utf-8').strip().replace('\n','').replace(';','') # utf-8 string
        item['authors']=filter(None,[n.encode('utf-8').strip().replace('\n','').replace(';','') for n in authors]) # utf-8 list
        #journal
        journal=sel.xpath('//*[name()="prism:publicationName"]//text()').extract()
        if journal==[]:
            journalname=''
        else:
            journalname=journal[0]
        item['journal']=journalname.strip().replace('\n','').replace(';','').encode('utf-8') # utf-8 string
        # date
        item['date']=datejoin.encode('utf-8') # utf-8 string
        #keytext
        words=[wd.strip().replace('\n','') for wd in words if len(wd)<100]
        keytext=c_join(words).replace('/','<>').replace(';','<>').replace(',','<>')
        item['keytext']=c_join(filter(None,[m.strip() for m in keytext.split('<>')])).encode('utf-8') # utf-8 string
        item['neoKeytexts']=item['keytext'].split('<>') # UTF-8 list
        #keywords
        words=list(set(words))
        item['keywords']=functions.lemma_listwords(words) # utf-8 list
        item['keywords']=list(set(item['keywords'])) # UTF-8 list

        return
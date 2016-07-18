from __future__ import print_function

import mysql.connector
from mysql.connector import errorcode
import save_txt
from random import randint
import codecs
import distance
import urllib2,urllib
from lxml import html
from PIL import Image
import numpy as np
import io
import plot
import im_combine
import process_text


#input ref-a word, allwords-a word list
# output a word list, sorted by similarity with the ref word
def P_S_P(ref,allwords):
    ref=process_text.lemma_listwords([ref])[0]
    allwords_lem=process_text.lemma_listwords([n.decode('utf-8') for n in allwords])
    value=[]
    for i,n in enumerate(allwords_lem):
        num=0
        reflist=ref.split(' ')
        testlist=n.split(' ')
        num=len(set(reflist).intersection(testlist))
        if num==0:
            value.append([num,''])
            continue
        else:
            value.append([num,allwords[i]])


    sort=sorted(value,key=lambda s: s[0],reverse=True)
    return sort







class Association:
    def __init__(self,kw_table,p2p_table,num):
        #kw_table string
        #p2p_table string
        #num int
        self.cnx = mysql.connector.connect(user='root',password='Lostyourface123',database='keywords_linkage')#,host='129.31.218.122')
        self.cursor = self.cnx.cursor()
        self.kw_table=kw_table
        self.p2p_table=p2p_table
        self.num=num
        self.showed=[]
        self.inputword=''
        #get allwords
        query="SELECT `word` FROM `{}`".format(self.kw_table)
        self.cursor.execute(query)
        self.allwords=[]
        for n in self.cursor:
            self.allwords.append(n[0].encode('utf-8'))

        self.N=len(self.allwords)

        self.H_V=0 #indication of the direction of image to show

        self.imgwhole=[] #whole image saved in memory
        self.imgw=[] # corresponding words of the image


        self.cnx.commit()
        self.cnx




    def make_associations(self,inputword):
        self.imgwhole=[]#clear image
        self.imgw=[]#clear corresponding words

        self.inputword=inputword
        #lower case
        self.inputword=self.inputword.lower()

        #!!!!!!!!!!!!!
        #lemmatize
        #self.inputword=process_text.lemma_listwords([self.inputword])[0]


        #no input random words
        if self.inputword=='':
            #get random int
            self.key_id=randint(0,self.N-1)
            self.mid_W=self.allwords[self.key_id]
            self.clearwords=['','','']
        else:
            #inputword in allwords
            if self.inputword in self.allwords:
                self.mid_W=self.inputword

                #get all related words, relatedwords include self.mid_W
                query='SELECT `col`,`value` FROM `{}` where `row`="{}" order by `value` DESC'.format(self.p2p_table,self.mid_W)
                self.cursor.execute(query)
                self.relatedwords=[]
                for n in self.cursor:
                    self.relatedwords.append(n[0].encode('utf-8'))




                #set up clear word
                self.clearwords=[]

                #append relatedword
                for n in self.relatedwords: #relatedwords include mid_W
                    if n not in [i for j in self.showed for i in j]: #delete showed word
                        self.clearwords.append(n) #clearwords may include mid_W
                    if len(self.clearwords)==self.num+1:
                        break


                #remove self.mid_W in clearwords
                if self.mid_W in self.clearwords:
                    self.clearwords.remove(self.mid_W)


                if len(self.clearwords)<self.num: # not enough clearwords
                    self.PSPwords=P_S_P(self.mid_W,self.allwords)  #get all PSP words, PSPwords include self.mid_W
                    #append P_S_P
                    for n in self.PSPwords:
                        if (n[1] not in [i for j in self.showed for i in j]) and (n[1] not in self.relatedwords):
                            self.clearwords.append(n[1]) #words appended at this section have no mid_W, no showed, and no before
                        if len(self.clearwords)>self.num:
                            break


            else:  #inputword not in allwords
                self.mid_W=self.inputword
                #clear showed words to zero
                #self.showed=[]
                #P to S, S to P
                self.PSPwords=P_S_P(self.mid_W,self.allwords)
                #clear words
                self.clearwords=[]
                for n in self.PSPwords:
                    if n[1] not in [i for j in self.showed for i in j]:
                        self.clearwords.append(n[1])
                    if len(self.clearwords)==self.num:
                        break

        self.step=[self.mid_W]
        for n in self.clearwords[0:self.num]:
            self.step.append(n)
        self.showed.append(self.step)

        return self.step


    def go_back(self):
        try:
            self.step=self.showed[-2]
        except:
            self.step=['','','','']

        try:
            self.showed.pop(-1)
        except:
            self.showed=[]
        return

    def restart(self):
        self.step=['','','','']
        self.showed=[]

        return



#download new words in words, and show image of words
    def GetImage(self,words):
        hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
               'Accept-Encoding': 'none',
               'Accept-Language': 'en-US,en;q=0.8',
               'Connection': 'keep-alive'}

        urllists=[]
        self.img=[] #image to show

        #images of word need to be downloaded
        down_words=list(set(words).difference(set(self.imgw)))



        for n in down_words:
            urlline="https://www.google.co.uk/search?site=&tbm=isch&q="+n.replace(' ','+')
            urllists.append(urlline)
        for inum,site in enumerate(urllists):
            req = urllib2.Request(site, headers=hdr)
            try:
                page = urllib2.urlopen(req)
            except:
                continue
            content=page.read()
            tree=html.fromstring(content)
            imageurls= tree.xpath('//div[@class="rg_di rg_el ivg-i"]/a/@href')
            for n in imageurls:
                URL= n.split('=')[1].split('&')[0]
                URL=urllib.unquote(urllib.unquote(URL))
                reqimg=urllib2.Request(URL, headers=hdr)
                try:
                    pageimg=urllib2.urlopen(reqimg, timeout=2.0)
                except:
                    continue

                try:
                    image_file = io.BytesIO(pageimg.read())
                except:
                    continue

                try:
                    pil_image = Image.open(image_file)
                except:
                    continue
                else:
                    pil_image=pil_image.convert('RGB')
                    open_cv_image = np.array(pil_image)
                    image = open_cv_image[:, :, ::-1].copy()
                    self.imgwhole.append(image)
                    self.imgw.append(down_words[inum])
                    break

        for m in words:
            try:
                self.img.append(self.imgwhole[self.imgw.index(m)])
            except:
                continue

        if len(words)==1:
            plot.im_plot(self.img,[],words[0],0)

        if len(words)>=2:
            if self.H_V==0:
                if len(words)==2:
                    Rec_Tri=randint(0,2)
                    if Rec_Tri==2:
                        im=im_combine.direct_Hcon(self.img)
                    else:
                        im=im_combine.HTri(self.img)
                else:
                    im=im_combine.direct_Hcon(self.img)

            if self.H_V==1:
                if len(words)==2:
                    Rec_Tri=randint(0,2)
                    if Rec_Tri==2:
                        im=im_combine.direct_Vcon(self.img)
                    else:
                        im=im_combine.VTri(self.img)
                else:
                    im=im_combine.direct_Vcon(self.img)

            showtext=words[0]
            for n in words[1:]:
                showtext=showtext+', '+n

            plot.im_plot([im],[],showtext,0)



        self.H_V=list(set([0,1]).difference(list([self.H_V])))[0]

        return
























'''
def P_S_P(ref,allwords):
    dif=[] #save distance for each word in allwords
    ref=ref.lower() # transfer to lower cases
    for n in allwords:
        D=0 #distance of one word in allwords
        allsmall=[] # store all small
        for i in ref.split(' '):
            subw=[] #store all j for i
            for j in n.split(' '):
                subw.append(distance.nlevenshtein(i,j))
            allsmall.append(min(subw)) #allsmall=smallest in every i
            D=D+min(subw) #add smalllest in every i
        D=D-0.9*(max(allsmall)-min(allsmall))
        dif.append([D,n])
    sort_dif=sorted(dif,key=lambda s: s[0])
    return sort_dif
'''
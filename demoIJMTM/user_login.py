from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.alert import Alert
import time
from lxml import html
from datetime import date


class APIKey:
    #spidername is string
    #oldkey is string
    #self.newkey is a string, which is the new APIKey of this spider
    def getAPIKey(self,spidername,oldkey):
        self.driver=webdriver.Chrome("C:/Python27/Lib/site-packages/selenium/webdriver/chrome/chromedriver.exe")
        #binary = FirefoxBinary('C:/Program Files (x86)/Mozilla Firefox/firefox.exe')
        #driver = webdriver.Firefox(firefox_binary=binary)

        #login
        self.driver.get("http://www.developers.elsevier.com/action/devprojects?originPage=devportal")

        #element = driver.find_element_by_xpath("//ul[@class='nav navbar-nav navbar-right']/li/a")
        #element.click()
        #driver.get('http://www.developers.elsevier.com/action/devprojects?originPage=devportal')

        elementlogin=self.driver.find_element_by_xpath("//li[@class='login']/a[@id='loginPlus']")
        elementlogin.click()

        eleusername=self.driver.find_element_by_xpath("//input[@id='username']")
        eleusername.send_keys("f.shi14@imperial.ac.uk")

        elepass=self.driver.find_element_by_xpath("//input[@id='password']")
        elepass.send_keys("Lostyourface123")

        elementsubmit=self.driver.find_element_by_xpath("//input[@value='Login']")
        elementsubmit.click()

    #delete
        time.sleep(5)
        eledelete=self.driver.find_element_by_xpath("//a[@id='{}']".format("apiDelHolder_1"))
        eledelete.click()
        time.sleep(5)
        self.delt=0
        while(self.delt==0):
            try:
                Alert(self.driver).accept()
            except:
                time.sleep(5)
            else:
                self.delt=1

        time.sleep(20)
        #alert = driver.switch_to_alert()
        #alert.accept()
        self.back=0
        while(self.back==0):
            try:
                elementsubmit=self.driver.find_element_by_xpath("//input[@class='txtSmaller']")
            except:
                time.sleep(20)
            else:
                self.back=1



    #apply

        elementsubmit=self.driver.find_element_by_xpath("//input[@class='txtSmaller']")
        elementsubmit.click()

        time.sleep(10)
        self.reg=0
        while(self.reg==0):
            try:
                eleweb=self.driver.find_element_by_xpath('//input[@id="applicationName"]')
            except:
                time.sleep(10)
            else:
                self.reg=1

        eleweb.send_keys(spidername)



        elecheck=self.driver.find_element_by_xpath('//input[@id="agreed"]')
        elecheck.click()

        eleregister=self.driver.find_element_by_xpath('//input[@type="submit"]')
        eleregister.click()

        time.sleep(20)
        self.extr=0
        while(self.extr==0):
            try:
                self.tree=html.fromstring(self.driver.page_source)
            except:
                time.sleep(10)
            else:
                #try:
                self.newid=self.tree.xpath('//input[@value="http://{}"]/@id'.format(spidername))[0]
                #except:
                #    eleregister=self.driver.find_element_by_xpath('//input[@type="submit"]')
                #    eleregister.click()
                #    time.sleep(20)
                #else:
                self.extr=1


        #self.newid=self.tree.xpath('//input[@value="http://{}"]/@id'.format(spidername))[0]
        self.newid=self.newid.replace('fullUrl','apiKeyHolderval')
        self.newkey=self.tree.xpath('//input[@id="{}"]/@value'.format(self.newid))[0]

        self.driver.close()


    def recursive_APIKey(self,spidername,oldkey,n):
        if n>5:
            print "Hey dude, can't do this anymore!!"
            return 0

        try:
            self.getAPIKey(spidername,oldkey)
        except:
            print 'Trial {}'.format(n)
            self.driver.close()
            return self.recursive_APIKey(spidername,oldkey,n+1)
        else:
            return 1


def Check_update_count(dc,count,limit):
    # update today
    dc["today"]["date"]=date.today()
    dc["today"]["count"]=count

    #calculate difference between today and lastday
    difcount=dc["today"]["count"] - dc["lastday"]["count"]
    difday=(dc["today"]["date"]-dc["lastday"]["date"]).days

    if difcount >= limit:
        return  True
    else:
        #update lastday
        if difday==7:
            dc["lastday"]["date"]=dc["today"]["date"]
            dc["lastday"]["count"]=dc["today"]["count"]

        return False
















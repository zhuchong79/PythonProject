# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import sys, urllib
import random
import socket
import urllib2
import cookielib

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
#获取csdn网页内容
import sys
reload(sys)
sys.setdefaultencoding('utf8')
class BrowserBase(object):
    def __init__(self):
        socket.setdefaulttimeout(20)

    def speak(self,name,content):
        print '[%s]%s' %(name,content)

    def openurl(self,url):
        """
        打开网页
        """
        cookie_support= urllib2.HTTPCookieProcessor(cookielib.CookieJar())
        self.opener = urllib2.build_opener(cookie_support,urllib2.HTTPHandler)
        urllib2.install_opener(self.opener)
        user_agents = [
                   'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
                   'Opera/9.25 (Windows NT 5.1; U; en)',
                   'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
                   'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
                   'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
                   'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
                   "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
                   "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 "
                   ]
        agent = random.choice(user_agents)
        self.opener.addheaders = [("User-agent",agent),("Accept","*/*"),('Referer','http://www.google.com')]
        try:
            res = self.opener.open(url)
            return res.read()
        except Exception,e:
            self.speak(str(e)+url)
            raise Exception

class Html2PDF(object):
    content=''
    title=''
    removeattr = ['#digg',"div[class='ad_class']","div[class='bdsharebuttonbox tracking-ad']","div[class='article_manage clearfix']",]
    def __init__(self,url):
        self.content = self.GetContent(url);
    def GetContent(self,url):
        return BrowserBase().openurl(url)
    def Process(self):
        #self.content = htmlcontent
        #f1=open('1.html','w')
        #f1.write(self.content)
        self.ModifyContent()
        self.SaveContentToPDF()
    def Analyse(self):
        soup = BeautifulSoup(unicode(self.content),"html5lib")
        open('fadf.html','w').write(self.content)
        for arc in soup.select("div[class='article_title']"):
            for add1 in arc.select('a'):
                print add1['href'].strip() +u'\t' + add1.string.strip() #add1.string.strip()
        for s in soup.select("div[id='papelist']"):
            for ss in s.select('a'):
                print ss

    def ModifyContent(self):
        print "ModifyContent begin..."
        soup = BeautifulSoup(unicode(self.content), "html5lib")
        self.title = (soup.find(class_='link_title').a.string).strip()
        removeattr = ['#side','#digg',"div[class='ad_class']","div[class='bdsharebuttonbox tracking-ad']","div[class='article_manage clearfix']",]
        for attr in removeattr:
            for sd in soup.select(attr):
                sd.decompose()
        for scripts in soup.find('script'):
            scripts.decompose()
        self.content = (soup.prettify()).encode('utf-8','ignore')
        #open('1.html','w').write(self.content)
        print "ModifyContent end..."
    def SaveContentToPDF(self):
        print "SaveContentToPDF begin..."
        app = QApplication(sys.argv)
        web = QWebView()
        web.setContent(self.content)
        printer = QPrinter()
        printer.setPageSize(QPrinter.A4)
        printer.setOutputFormat(QPrinter.PdfFormat)
        filetitle=self.title+u'.pdf'
        print filetitle
        printer.setOutputFileName(filetitle)

        def convertIt():
            web.print_(printer)
            print "Pdf generated"
            QApplication.exit()

        QObject.connect(web, SIGNAL("loadFinished(bool)"), convertIt)
        sys.exit(app.exec_())
        print "SaveContentToPDF end..."
if __name__ == '__main__':
    #browser = BrowserBase();
    #content=browser.openurl('http://blog.csdn.net/y_csdnblog_xx/article/details/51480342')

    ss=Html2PDF('http://blog.csdn.net/y_csdnblog_xx/article/category/6241136')
    ss.Analyse()
    print 'ok'
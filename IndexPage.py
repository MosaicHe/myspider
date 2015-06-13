#!/usr/bin/python
#!-*-coding:utf8-*-

import urllib2
import StringIO,gzip
from sgmllib import SGMLParser
import os
import re

class ParserHtml(SGMLParser):
    def reset(self):
        self.h3_flag=False
        self.url_list=[]
        SGMLParser.reset(self)

    def start_h3(self,attrs):
        self.h3_flag=True

    def end_h3(self):
        self.h3_flag=False

    def start_a(self, attrs):
        if self.h3_flag:
            hrel=[v for k,v in attrs if k=="href"]
            if hrel:
                self.url_list.extend(hrel)

def gzdecode(data):
    compressedstream = StringIO.StringIO(data)
    gziper = gzip.GzipFile(fileobj=compressedstream)
    data2 = gziper.read()
    return data2


class IndexPage(object):
    def __init__(self, url):
        self.index_url=url
        self.htmlContent=""
        self.urls=[]
        self.headers={
            "Host":"cl.bearhk.info",
            "Connection":"keep-alive",
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
            "Accept-Encoding":"gzip, deflate, sdch",
            "Accept-Language":"zh-CN,zh;q=0.8",
            "Cookie":"__cfduid=d85f67776754f2f8889f05449af0967d91433699473; CNZZDATA950900=cnzz_eid%3D1154953464-1433695251-%26ntime%3D1433780060",
            "If-None-Match":'W/"1e833fa-229b-518048e8e1455"',
            "If-Modified-Since":"Mon, 09 Jun 2015 16:58:54 GMT",
        }

    def initial(self):
        req=urllib2.Request(self.index_url, headers=self.headers)
        try:
            response=urllib2.urlopen(req)
        except urllib2.URLError,e:
            if hasattr(e,"reason"):
                print "Failed to reach the server"
                print "The reason:",e.reason
            elif hasattr(e,"code"):
                print "The server couldn't fulfill the request"
                print "Error code:",e.code
                print "Return content:",e.read()
        else:
            content = response.read()
            self.htmlContent=gzdecode(content)
            #print(self.htmlContent)
            parserhtml=ParserHtml()
            parserhtml.feed(self.htmlContent)
            self.urls=parserhtml.url_list
            #print(self.urls)

def getIndexPageUrls(url):
     m = IndexPage(url)
     m.initial()
     #print(m.urls)
     return m.urls

if __name__=="__main__":
    url="http://cl.bearhk.info/thread0806.php?fid=15&search=&page=1"
    m = IndexPage(url)
    m.initial()
    print(m.urls)




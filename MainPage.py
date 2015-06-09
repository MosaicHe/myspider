#!/usr/bin/python
#!-*-coding:utf8-*-

import urllib2
import StringIO,gzip
from sgmllib import SGMLParser
import os
import re


headers={
            "Host":"cl.bearhk.info",
            "Connection":"keep-alive",
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
            "Accept-Encoding":"gzip, deflate, sdch",
            "Accept-Language":"zh-CN,zh;q=0.8",
            "Cookie":"__cfduid=d85f67776754f2f8889f05449af0967d91433699473; CNZZDATA950900=cnzz_eid%3D1154953464-1433695251-%26ntime%3D1433780060",
            "If-None-Match":'W/"1e833fa-229b-518048e8e1455"',
            "If-Modified-Since":"Mon, 08 Jun 2015 16:58:54 GMT",
            }

def gzdecode(data):
    compressedstream = StringIO.StringIO(data)
    gziper = gzip.GzipFile(fileobj=compressedstream)
    data2 = gziper.read()
    return data2

class ParserHtml(SGMLParser):
    def reset(self):
        self.flag = False
        self.title=""
        self.title_flag=False
        self.url = ""
        self.picture=[]
        SGMLParser.reset(self)

    def start_title(self,attrs):
        self.title_flag=True

    def end_title(self):
        self.title_flag=False

    def start_a(self, attrs):
        self.flag= True

    def end_a(self):
        self.flag = False

    def start_img(self, attrs):
        pic=[v for k,v in attrs if k=="src" and v.find(".jpg")!=-1]
        if(pic):
            self.picture.extend(pic)

    def handle_data(self, data):
        if self.flag:
            #print data
            if(data.find("hash=")!=-1):
                self.url=data
        if self.title_flag:
            self.title=data

def getHtmlContent(url):
    req=urllib2.Request(url, headers=headers)
    content = urllib2.urlopen(req).read()
    #print(content)
    buf = gzdecode(content)
    #print(buf)
    return buf

__g_content__=""
parserhtml = ParserHtml()

def init_html(url):
    global __g_content__
    if(__g_content__==""):
        __g_content__=getHtmlContent(url)
    parserhtml.feed(__g_content__)
    #os.mkdir("picture")

def getUrl(url):
    global __g_content__
    if(__g_content__==""):
        print("content is not initial")
    return parserhtml.url
    #return listname.input_dict, listname.action

def download_picture():
    pic_num=0
    for url in parserhtml.picture:
        req=urllib2.Request(url, headers=headers)
        content = urllib2.urlopen(req).read()
        #os.chdir("picture")
        name="%d.jpg"%pic_num
        f=open( name, "wb")
        f.write(content)
        f.close()

if __name__=="__main__":
    url="http://cl.bearhk.info/htm_data/15/1506/1514302.html"
    init_html(url)
    #download_url=getUrl(url)
    #print(download_url)

    download_picture()
    #os.mkdir()
    #download_picture()
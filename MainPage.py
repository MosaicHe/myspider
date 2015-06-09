#!/usr/bin/python
#!-*-coding:utf8-*-

import urllib2
import StringIO,gzip
from sgmllib import SGMLParser
import os
import re

import DownloadTorrent
import GetFormData


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
            if(data.find("hash=")!=-1):
                self.url=data

        if self.title_flag:
            #print(data.decode("GBK").encode("utf8"))
            self.title=data.decode("GBK").encode("utf8")

def gzdecode(data):
    compressedstream = StringIO.StringIO(data)
    gziper = gzip.GzipFile(fileobj=compressedstream)
    data2 = gziper.read()
    return data2


class MainPage(object):
    def __init__(self, url):
        self.url=url
        self.fileDir=""
        self.pic_url=[]
        self.torrent_url=""
        self.htmlContent=""
        self.parserhtml=ParserHtml()
        self.headers={
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

    def initial(self):
        req=urllib2.Request(self.url, headers=self.headers)
        response = urllib2.urlopen(req)
        #print(content)
        #print(response.info())
        self.htmlContent = gzdecode(response.read())
        self.parserhtml.feed(self.htmlContent)
        self.torrent_url=self.parserhtml.url
        self.pic_url=self.parserhtml.picture
        self.fileDir=self.parserhtml.title.split('  ')[0].split(']')[1].replace('/','-').replace(' ', '-')
        #print(self.fileDir)
        #print(self.pic_url)
        #dirlist=os.listdir('.')
        os.mkdir(self.fileDir)
        os.chdir(self.fileDir)

    def download_picture(self):
        pic_num=1
        for url in self.pic_url:
            req=urllib2.Request(url, headers=self.headers)
            content = urllib2.urlopen(req).read()
            name="%d.jpg"%pic_num
            pic_num+=1
            f=open( name, "wb")
            f.write(content)
            f.close()

    def download_torrent(self):
        formdata=GetFormData.FormData()
        form,action=formdata.getformdata( self.torrent_url )
        torrent_url="http://www.rmdown.com/"+action
        download=DownloadTorrent.Download_Torrent()
        download.download_torrent(torrent_url, form)

if __name__=="__main__":
    url="http://cl.bearhk.info/htm_data/15/1506/1514302.html"
    m = MainPage(url)
    m.initial()
    m.download_picture()
    m.download_torrent()


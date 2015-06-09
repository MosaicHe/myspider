#!/usr/bin/python
#!-*-coding:utf8-*-

import urllib2
import StringIO,gzip
from sgmllib import SGMLParser

from sgmllib import SGMLParser


class FormData(object):

    def __init__(self):
        pass

    class GetIdList(SGMLParser):
        def reset(self):
            self.flag = False
            self.input_dict = {}
            self.action=""
            SGMLParser.reset(self)

        def start_form(self, attrs):
            self.flag= True
            for k,v in attrs:
                if(k=="action"):
                    self.action=v

        def end_form(self):
            self.flag = False

        def start_input(self,attrs):
            if(self.flag):
                name=""
                val=""
                for k, v in attrs:
                    if(k=="name" ):
                        name=v
                    elif(k=="value"):
                         val=v
                    if(name!="" and val !=""):
                        self.input_dict[name]=val


    def gzdecode(self,data):
        compressedstream = StringIO.StringIO(data)
        gziper = gzip.GzipFile(fileobj=compressedstream)
        data2 = gziper.read()
        return data2

    def getformdata(self, url):
        headers={
                "Host":"www.rmdown.com",
                "User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0",
                "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language":"en-US,en;q=0.5",
                "Accept-Encoding":"gzip, deflate",
                "Cookie":"cfduid=d09dcfb46e56a000de2739f97456f2ef31433760629",
                "Connection":"keep-alive",
                }

        req=urllib2.Request(url, headers=headers)
        content = urllib2.urlopen(req).read()
        buf=self.gzdecode(content)
        listname = self.GetIdList()
        listname.feed(buf)
        return listname.input_dict, listname.action

if(__name__=="__main__"):
    url="http://www.rmdown.com/link.php?hash=1525dd669aba737c4f110fc8bcd173b67adedd3051e"
    formdata=FormData()
    print(formdata.getformdata(url))




import urllib2,urllib
import StringIO,gzip
import re

class Download_Torrent():
    def gzdecode(self, data):
        compressedstream = StringIO.StringIO(data)
        gziper = gzip.GzipFile(fileobj=compressedstream)
        data2 = gziper.read()
        return data2

    def http_request(self, url, headers, postdata):
        #FIXME, add error catch
        req = urllib2.Request(url,headers=headers,data=postdata)
        response= urllib2.urlopen(req)
        return response.read(), response.info()

    def download_torrent(self, url, form):
        boundary = "----WebKitFormBoundarydMcOM7W0mij63Igr"
        parts=[]
        for k,v in form.items():
            parts.append('--' + boundary)
            parts.append('Content-Disposition: form-data; name="'+k+'"')
            parts.append('')
            parts.append(v)
        parts.append('--' + boundary + '--')
        parts.append('\r\n')
        postdata = '\r\n'.join(parts)

        headers={ "Host":"www.rmdown.com",
                  "Cache-Control":"max-age=0",
                  "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
                  "Connection":"keep-alive",
                  "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                  "Accept-Encoding":"gzip, deflate",
                  "Accept-Language":"zh-CN,zh;q=0.8",
                  "ContWebKitFormBoundarydMcOM7W0mij63Igrent-Type":"multipart/form-data; boundary="+boundary,
                  "Cookie":"__cfduid=de4cec1ae2907c5fe4e3a3e9e68f4f5e01433688027"
                }
        html, response_header=self.http_request(url, headers, postdata)
        data=urllib.urlencode(form)
        html, response_header=self.http_request(url, headers, data)
        filename=form['ref']+".torrent"
        buf=self.gzdecode(html)
        f=open(filename, "wb")
        #f.write(response.info()["Set-Cookie"])
        f.write(buf)
        f.close()
        return 0

if __name__=="__main__":
    url="http://www.rmdown.com/download.php"
    form={'ref': '1525dd669aba737c4f110fc8bcd173b67adedd3051e', 'submit': 'download', 'reff': 'MTQzMzc3ODk0Mg=='}
    download=Download_Torrent()
    download.download_torrent(url, form)






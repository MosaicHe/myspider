import IndexPage
import MainPage

url="http://cl.bearhk.info/thread0806.php?fid=15&search=&page=1"
#get url list from index page
mp_urllist=IndexPage.getIndexPageUrls(url)

for url in mp_urllist:
    MainPage.exec_download("http://cl.bearhk.info/"+url)

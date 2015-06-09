import GetFormData
import DownloadTorrent
import MainPage

url="http://cl.bearhk.info/htm_data/15/1506/1514015.html"

download_url=MainPage.getUrl(url)

formdata=GetFormData.FormData()
form,action=formdata.getformdata(download_url)

torrent_url="http://www.rmdown.com/"+action
download=DownloadTorrent.Download_Torrent()
download.download_torrent(torrent_url, form)
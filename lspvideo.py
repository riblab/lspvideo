import requests
from lxml import etree

link = input('输入要下载的梨视频了链接：')
resp = requests.get(link)
resp.close

# 拿到视频名称
tree = etree.HTML(resp.text)
title = tree.xpath('/html/head/title/text()')[0].strip("-梨视频官网-Pear Video")

# 获取请求地址
url = link.split("_")[1]
videoStatus = f"https://pearvideo.com/videoStatus.jsp?contId={url}&mrd=0.9254047947274395"

# 拿到伪地址，过防盗链
headers = {
    "Referer": link,
}
resp = requests.get(videoStatus,headers=headers)

dic = resp.json()
systemTime = dic['systemTime']
srcUrl = dic['videoInfo']['videos']['srcUrl']

# 替换真实地址
srcUrl = srcUrl.replace(systemTime,f"cont-{url}")

# 下载视频
with open(f'{title}-riblab.mp4',mode='wb') as f:
    f.write(requests.get(srcUrl).content)
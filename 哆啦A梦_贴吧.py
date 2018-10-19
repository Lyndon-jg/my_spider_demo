import urllib.request
import urllib.parse
import random
from lxml import etree

#tiezi_link://div[@class="threadlist_lz clearfix"]//a[@class="j_th_tit "]/@href

def loadPage(url):
    """
    函数说明：根据url发送请求，获取服务器响应文件
    url:需要爬取的URL地址
    """
    UA = [
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.2)',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)'
    ]
    ua = random.choice(UA)
    header = {'User-Agent': ua}
    request = urllib.request.Request(url, headers=header)
    html = urllib.request.urlopen(request).read()
    # 解析html文档为HTML DOM模型
    content = etree.HTML(html)
    # 返回所有匹配成功的列表集合
    link_list = content.xpath('//div[@class="threadlist_lz clearfix"]//a[@class="j_th_tit "]/@href')
    for link in link_list:
        full_link = 'https://tieba.baidu.com' + link
        print(full_link)
        loadImage(full_link)

def loadImage(link):
    """
    函数说明：取出每个帖子中的图片链接
    link:图片链接
    """
    header = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)'}
    request = urllib.request.Request(link, headers=header)
    html = urllib.request.urlopen(request).read()
    # 解析html文档为HTML DOM模型
    content = etree.HTML(html)
    # 返回帖子里所有图片链接
    link_list = content.xpath('//img[@class="BDE_Image"]/@src')
    for link in link_list:
        print(link)
        writeImage(link)

def writeImage(link):
    """
    函数说明：将图片写入到本地
    link:图片链接
    """
    header = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)'}
    request = urllib.request.Request(link, headers=header)
    image = urllib.request.urlopen(request).read()
    filename = link[-10:]
    with open(filename, 'wb') as f:
        f.write(image)

def tiebaSpider(url, beginPage, endPage):
    """
        函数说明：贴吧爬虫调度器，负责组合处理每个页面的url
        url:贴吧url的前部分
        beginPage：起始页
        endPage：终止页
    """
    for page in range(beginPage, endPage + 1):
        pn = (page - 1) * 50
        fullurl = url + '&pn=' + str(pn)
        loadPage(fullurl)

    print('game over')

if __name__ == '__main__':
    kw = input('input teiba name:')
    beginPage = int(input('beginPage:'))
    endPage = int(input('endPage'))

    url = 'https://tieba.baidu.com/f?'
    key = urllib.parse.urlencode({'kw': kw})
    fullurl = url + key
    print(fullurl)
    tiebaSpider(fullurl, beginPage, endPage)


import urllib.request
import random
from lxml import etree


class DownLoadNovel(object):

    def __init__(self):
        self.file_name = '九界天君.txt'
        # ie User-Agent
        self.ua = [
            'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.2)',
            'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)'
        ]
        self.header = {'User-Agent': random.choice(self.ua)}
        # 目标URL
        self.url = 'http://book.zongheng.com/showchapter/708968.html'
        # 网页源码
        self.html = ''
        # 章节名称
        self.names = []
        # 章节URL
        self.urls = []
        self.nums = 0

    def get_urls(self):
        """
        函数说明：获取小说各个章节URL
        """
        request = urllib.request.Request(url=self.url, headers=self.header)
        response = urllib.request.urlopen(request)
        self.html = response.read()
        # 解析html文档为HTML DOM模型
        html = etree.HTML(self.html)
        self.urls = html.xpath('//li[@class=" col-4"]/a/@href')
        self.names = html.xpath('//li[@class=" col-4"]/a/text()')
        self.nums = len(self.urls)
        for i in range(self.nums):
            self.get_contents(name=self.names[i], link=self.urls[i])

    def get_contents(self, name, link): 
       """
        函数说明：获取各个章节内容
        name:章节名称
        link:每页链接
        """
        request = urllib.request.Request(url=link, headers=self.header)
        response = urllib.request.urlopen(request)
        self.html = response.read()
        # 解析html文档为HTML DOM模型
        html = etree.HTML(self.html)
        contents = html.xpath('//div[@class="content"]/p/text()')
        self.write_contents(name=name, content=contents)

    def write_contents(self, name, content):
       """
        函数说明：将章节内容写入本地文件
        name:章节名称
        content:章节内容
        """
        with open(self.file_name, 'a', encoding='utf-8') as f:
            f.write(name + '\n')
            f.writelines(content)
            f.write('\n\n')


if __name__ == '__main__':
    down_loader = DownLoadNovel()
    down_loader.get_urls()
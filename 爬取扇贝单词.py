import urllib.request
import random
from lxml import etree


class DownLoadWords(object):
    '''
    下载扇贝六级单词
    '''
    def __init__(self):
        self.host = 'https://www.shanbay.com'
        self.target = 'https://www.shanbay.com/wordbook/162079/'
        # 章节链接
        self.chapter_links = []
        # 章节名称
        self.chapter_names = []
        # 各章节单词
        self.words = []
        # 单词翻译
        self.translate = []
        self.User_Agent = [
            'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.2)',
            'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)'
        ]
        self.ua = random.choice(self.User_Agent)
        self.header = {
            'Connection': 'keep - alive',
            'Upgrade - Insecure - Requests': '1',
            'User - Agent': self.ua,
            'Accept': 'text/html,application/xhtml+xml, application/xml;q=0.9,image/webp,image/apng,*/*;q = 0.8',
            'Referer': 'https://www.shanbay.com/wordbook/books/mine/',
            'Accept - Language': 'zh-CN,zh;q=0.9',
            'Cookie': 'xxxxxxxxxxxxxxxxx'
        }

    def get_words_links(self):
        """
        函数说明：在target界面获取单词的链接
        """
        request = urllib.request.Request(url=self.target, headers=self.header)
        response = urllib.request.urlopen(request)
        # 读取html中的内容
        html = response.read()
        # 解析html为DOM html文档
        html = etree.HTML(html)
        # 解析出存放单词的链接
        self.chapter_links = html.xpath('//td[@class="wordbook-wordlist-name"]/a/@href')
        # 解析出存放单词的章节名称
        self.chapter_names = html.xpath('//td[@class="wordbook-wordlist-name"]/a/text()')
        for num in range(len(self.chapter_links)):
            self.get_words(url=self.chapter_links[num], name=self.chapter_names[num])
            print('write chapter 1 ok')

    def get_words(self, url, name):
        """
        函数说明：获取每个URL下的单词
        :param url: 单词所在的URL
        :param name: 单词所在的章节名称
        """
        for page in range(1, 11):
            request = urllib.request.Request(url=self.host + url + '?page' + str(page), headers=self.header)
            response = urllib.request.urlopen(request)
            # 读取html中的内容
            html = response.read()
            # 解析html为DOM html文档
            html = etree.HTML(html)
            # 解析出每页的英文单词
            self.words = html.xpath('//tr[@class="row"]/td[@class="span2"]/strong/text()')
            self.translate = html.xpath('//tr[@class="row"]/td[@class="span10"]/text()')
            self.write_words(name + '__page__' + str(page))

    def write_words(self, name):
        """
        函数说明：将单词写入words.txt中
        :param name: 单词所在的章节名称
        """
        with open('words.txt', 'a+', encoding='utf-8') as f:
            f.write(name + '\n')
            f.writelines(self.words)
            f.write('\n\n')


if __name__ == '__main__':

    words_downloader = DownLoadWords()
    words_downloader.get_words_links()








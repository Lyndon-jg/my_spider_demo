import json
import requests
from lxml import etree


class ProxyMetaclass(type):
    def __new__(cls, name, bases, attrs):
        count = 0
        attrs['__CrawlFunc__'] = []
        for k, v in attrs.items():
            if 'crawl_' in k:
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(cls, name, bases, attrs)


class Crawler(object, metaclass=ProxyMetaclass):
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)'
        }

    def get_proxies(self, callback):
        proxies = []
        for proxy in eval('self.{}()'.format(callback)):
            print('成功获取到代理', proxy)
            proxies.append(proxy)
        return proxies

    def crawl_daili66(self, page_count = 4):
        """
        获取代理66
        :param page_count: 页码
        :return: 代理
        """
        target_url = 'http://www.66ip.cn/{}.html'
        for page in range(1, page_count + 1):
            if page == 1:
                page = 'index'
            url = target_url.format(page)
            print(url)
            response = requests.get(url, headers=self.headers)
            response.encoding = 'gb2312'
            html = response.text
            if html:
                dom = etree.HTML(html)
                trs = dom.xpath('//tr[position() > 1]')
                for tr in trs:
                    ip = tr.xpath('./td[1]/text()')[0]
                    port = tr.xpath('./td[2]/text()')[0]
                    yield ':'.join([ip, port])

    def crawl_xicidaili(self):
        for i in range(1, 3):
            start_url = 'http://www.xicidaili.com/nn/{}'.format(i)
            print(start_url)
            response = requests.get(start_url, headers=self.headers)
            html = response.text
            if html:
                dom = etree.HTML(html)
                trs = dom.xpath('//tr[position() > 1]')
                for tr in trs:
                    ip = tr.xpath('./td[2]/text()')[0]
                    port = tr.xpath('./td[3]/text()')[0]
                    yield ':'.join([ip, port])

# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from DongGuang.items import DongItem
import re


class SunSpider(CrawlSpider):
    name = 'sun'
    allowed_domains = ['wz.sun0769.com']
    start_urls = ['http://d.wz.sun0769.com/index.php/department?departmentid=63&page=0']

    # 每一页链接的匹配规则
    pagelink = LinkExtractor(allow=r'departmentid=63&page=\d+')
    # 每个帖子链接
    contentlink = LinkExtractor(allow=r'question/\d+/\d+.shtml')
    rules = (
        Rule(pagelink, process_links='dealLinks', follow=True),
        Rule(contentlink, follow=False, callback='parseDong')
    )

    def parseDong(self, response):
        item = DongItem()
        # 编号
        s = response.xpath('//div[@class="pagecenter p3"]//div/strong/text()').extract_first()
        item['num'] = s.strip().split(':')[1]
        # title
        item['title'] = s.split('\xa0')[0].split('：')[1]
        # 内容
        # 有内容则说明，有图片
        text = response.xpath('//div[@class="contentext"]/text()').extract()
        if len(text) == 0:
            # 取出无图片下的内容
            text = response.xpath('//div[@class="c1 text14_2"]/text()').extract()
        item['text'] = ''.join(text).replace(r'\xa0', '')
        # url
        item['url'] = response.url

        yield item

    # 需要重新处理每个response里提取的链接，去掉...&page=72后面的东西
    # links 就是linkextractor提取出来的页面链接列表
    def dealLinks(self, links):
        for link in links:
            link.url = re.match(r'.*page=\d+', link.url).group()
        # 返回修改完的links链接列表
        return links



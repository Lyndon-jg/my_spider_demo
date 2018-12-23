# -*- coding: utf-8 -*-
import scrapy
from ArticleSpider.items import JobBoleArticleItem, ArticleItemLoader
from urllib import parse
from ArticleSpider.utils.common import get_md5
from scrapy.loader import ItemLoader


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        image_url = response.xpath('//div[@id="archive"]/div[position()<last()]/div[1]//img/@src').extract_first()
        article_url = response.xpath('//div[@id="archive"]/div[position()<last()]/div[2]/p[1]/a[1]/@href').extract_first()
        if article_url:
            yield scrapy.Request(parse.urljoin(response.url, article_url),meta={'meta_1': image_url}, callback=self.parse_detail)

        next_page_url = response.xpath('//a[@class="next page-numbers"]/@href').extract_first()
        if next_page_url:
            yield scrapy.Request(parse.urljoin(response.url, next_page_url), callback=self.parse)

    def parse_detail(self, response):
        # item = ArticleItem()
        image_url = response.meta.get('meta_1')
        # item['title'] = response.xpath('//h1/text()').extract_first()
        # item['image_url'] = [image_url]
        # item['url_object_id'] = get_md5(image_url)
        # item['image_path'] = ''
        # 通过itemloader 加载 item
        item_loader = ArticleItemLoader(item=JobBoleArticleItem(), response=response)

        item_loader.add_xpath('title', '//h1/text()')
        item_loader.add_value('image_url', [image_url])
        item_loader.add_value('url_object_id', get_md5(image_url))
        item_loader.add_value('url_object_id', '')

        article_item = item_loader.load_item()
        yield article_item


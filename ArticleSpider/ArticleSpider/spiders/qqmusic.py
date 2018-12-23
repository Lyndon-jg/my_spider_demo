import scrapy
import random
import json
from ArticleSpider.items import QQMusicItemLoader, QQMusicItem


class QQMusicSpider(scrapy.Spider):
    name = 'qqmusic'
    allowed_domains = ['y.qq.com']
    start_urls = ['https://y.qq.com/portal/playlist.html']
    offset = 29



    def start_requests(self):
        for page in range(235):
            sin = page * 30
            ein = sin + self.offset
            url = self.creat_url(sin, ein)
            headers = {'referer': 'https://y.qq.com/portal/playlist.html'}
            yield scrapy.Request(url=url, callback=self.parse, headers=headers)

    def creat_url(self, sin, ein):
        def get_rnd():
            return random.random()
        return 'https://c.y.qq.com/splcloud/fcgi-bin/fcg_get_diss_by_tag.fcg?picmid=1&rnd=%s&g_tk=5381&jsonpCallback=getPlaylist&loginUin=0&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0&categoryId=10000000&sortId=5&sin=%s&ein=%s' % (get_rnd(), sin, ein)

    def create_detail_url(self, id):
        return 'https://c.y.qq.com/qzone/fcg-bin/fcg_ucc_getcdinfo_byids_cp.fcg?type=1&json=1&utf8=1&onlysong=0&disstid=%s&format=jsonp&g_tk=5381&jsonpCallback=playlistinfoCallback&loginUin=0&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0' % (id)

    def parse(self, response):
        json_text = json.loads(response.text[len('getPlaylist') + 1: -1])
        lists = json_text['data']['list']
        for each_list in lists:
            url = self.create_detail_url(each_list['dissid'])
            items = {}
            items['createTime'] = each_list['createtime']
            items['authorName'] = each_list['creator']['name']
            items['playTimes'] = each_list['listennum']
            items['songSheet'] = each_list['dissname']
            diss_id = each_list['dissid']
            headers = {'referer': 'https://y.qq.com/n/yqq/playsquare/%s.html' % (diss_id)}
            yield scrapy.Request(url=url, headers=headers, meta={'items': items}, callback=self.parse_detail)

    def parse_detail(self, response):
        items = response.meta.get('items', [])
        json_text = json.loads(response.text[len('playlistinfoCallback') + 1: -1])

        item_loader = QQMusicItemLoader(item=QQMusicItem(), response=response)

        item_loader.add_value('songSheet', items['songSheet'])
        item_loader.add_value('authorName', items['authorName'])
        item_loader.add_value('playTimes', items['playTimes'])
        item_loader.add_value('createTime', items['createTime'])
        item_loader.add_value('tags', json_text['cdlist'][0]['tags'])
        # json_text['cdlist'][0]['desc']
        item_loader.add_value('url', response.request.headers['referer'])

        item = item_loader.load_item()
        yield item

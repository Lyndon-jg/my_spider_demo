# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import JsonItemExporter
from twisted.enterprise import adbapi
import json
import csv
import codecs
import pymysql


class ArticlePipeline(object):
    def process_item(self, item, spider):
        return item


class MysqlPipeline(object):
    # 采用同步机制写入MySQL
    def __init__(self):
        self.conn = pymysql.connect(host='127.0.0.1', user='root', password='ljg', database='xxx', charset='utf-8', use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):

        insert_sql = ''
        self.cursor.execute(insert_sql, (item['title'], item['image_url']))
        self.conn.commit()


class MysqlTwistedPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host=settings['MYSQL_HOST'],
            user=settings['MYSQL_USER'],
            password=settings['MYSQL_PASSWD'],
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True
        )
        dbpool = adbapi.ConnectionPool('pymysql', **dbparms)
        return cls(dbpool)

    def process_item(self, item, spider):
        # 使用twisted将MySQL插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider)  # 处理异常

    #                           对应上一行最后的item spider
    def handle_error(self, failure, item, spider):
        # 处理异步插入的异常
        print(failure)

    def do_insert(self, cursor, item):
        # 执行具体的插入
        """ 不太好
        # 根据不同的item，构建不同的sql语句并插入到MySQL
        if item.__class__.__name__ == 'JobBoleArticleItem':
            insert_sql = ''
            self.cursor.execute(insert_sql, ('', ''))
        """
        insert_sql, params = item.get_insert_sql()
        cursor.execute(insert_sql, params)


class JsonWithEncodingPipeline(object):
    # 自定义json文件导出
    def __init__(self):
        self.file = codecs.open('article.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(lines)
        # 要return item, 下一个pipeline可能处理
        return item

    def close_spider(self, spider):
        self.file.close()


class JsonExporterPipeline(object):
    # 调用scrapy 提供的json export导出json文件
    def __init__(self):
        self.file = open('articleexport.json', 'wb')
        self.export = JsonItemExporter(self.file, encoding='utf-8', ensure_ascii=False)
        self.export.start_exporting()

    def process_item(self, item, spider):
        self.export.export_item(item)
        return item

    def close_spider(self, spider):
        self.export.finish_exporting()
        self.file.close()


class ArticleImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        if 'image_path' in item:
            for ok, value in results:
                iamge_file_path = value['path']
            item['image_path'] = iamge_file_path
        return item


# ------------------------QQMusic---------------------------------
class QQMusicPipeline(object):
    def __init__(self):
        self.f = open('QQMusic.csv', 'w')
        self.my_writer = csv.writer(self.f)

    def process_item(self, item, spider):
        values = [
            item['songSheet'],
            item['authorName'],
            item['playTimes'],
            item['createTime'],
            item['tags'],
            item['url']
        ]
        self.my_writer.writerow(values)

    def close_spider(self, spider):
        self.f.close()



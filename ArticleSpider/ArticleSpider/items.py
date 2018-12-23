# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join

# ------------------------jobbole---------------------------------

def add_jobbole(value):
    return value + '-jobbole'


class ArticleItemLoader(ItemLoader):
    # 自定义itemloader
    default_output_processor = TakeFirst()

def remove_comment_tages(value):
    # 去掉tag中提取的评论
    if '评论' in value:
        return ''
    else:
        return value

def return_value(value):
    return value


class JobBoleArticleItem(scrapy.Item):
    title = scrapy.Field(
        input_processor=MapCompose(add_jobbole, lambda x: x + '-booby'),
#        output_processor=TakeFirst()
    )
    image_url = scrapy.Field(
        output_processor=MapCompose(return_value)
    )
    image_path = scrapy.Field()
    url_object_id = scrapy.Field()
    Tags = scrapy.Field(
        input_processor=MapCompose(remove_comment_tages),
        output_processor=Join(',')
    )


# ------------------------QQMusic---------------------------------
def parse_tags(value):
    return value['name']


def convert_url(value):
    return value.decode('utf-8')


class QQMusicItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


class QQMusicItem(scrapy.Item):
    songSheet = scrapy.Field()
    authorName = scrapy.Field()
    playTimes = scrapy.Field()
    createTime = scrapy.Field()
    tags = scrapy.Field(
        input_processor=MapCompose(parse_tags),
        output_processor=Join(',')
    )
    url = scrapy.Field(
        input_processor=MapCompose(convert_url)
    )

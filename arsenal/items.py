# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ArsenalCardItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    full_text_url = scrapy.Field()
    card_header = scrapy.Field()
    card_content = scrapy.Field()
    card_small_photo = scrapy.Field()
    card_src = scrapy.Field()
    artical_id = scrapy.Field()


class ArsenalArticalItem(scrapy.Item):
    artical_id = scrapy.Field()
    artical_title = scrapy.Field()
    artical_src = scrapy.Field()
    artical_date = scrapy.Field()
    artical_important_pic = scrapy.Field()
    artical_main_content = scrapy.Field()
    artical_editor = scrapy.Field()
    artical_type = scrapy.Field()

# class ArsenalArticalReadItem(ArsenalArticalItem):
#     artical_type = scrapy.Field()


class ArsenalArticalVideoItem(ArsenalArticalItem):
    artical_video_play = scrapy.Field()

# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

# 项目中的item文件
"""
所谓Item容器就是将在网页中获取的数据结构化保存的数据结构，类似于Python中字典
"""
class BigdealsScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # 交易时间
    date = scrapy.Field()
    # 股票代码
    code = scrapy.Field()
    # 股票简称
    name = scrapy.Field()
    # 当前交易价格
    price = scrapy.Field()
    # 成交数量
    num = scrapy.Field()
    # 总成交金额
    totalPrice = scrapy.Field()
    # 买方
    buyer = scrapy.Field()
    # 卖方
    seller = scrapy.Field()
    # 证券类型
    type = scrapy.Field()

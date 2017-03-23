# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json


class BigdealsScrapyPipeline(object):
    """
    主要完成数据的查重、丢弃，验证item中数据，将得到的item数据保存等工作
    """
    def __init__(self):
        self.file = codecs.open('deal.json', 'wb', encoding='utf-8')


    def process_item(self, item, spider):
        """
        其中的process_item方法是必须调用的用来处理item，并且返回值必须为Item类的对象，或者是抛出DropItem异常
        :param item:
        :param spider:
        :return: Item类的对象
        """
        line = json.dumps(dict(item)) + '\n'
        print line
        self.file.write(line.decode("unicode_escape"))
        return item

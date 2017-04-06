# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
# import codecs
# import json
from twisted.enterprise import adbapi
import MySQLdb
import MySQLdb.cursors
import logging


class BigdealsScrapyPipeline(object):
    """
    主要完成数据的查重、丢弃，验证item中数据，将得到的item数据保存等工作
    """
    def __init__(self, dbpool):
        # self.file = codecs.open('deal.json', 'wb', encoding='utf-8')
        self.dbpool = dbpool
        logging.info("dbpool: " + str(dbpool))

    @classmethod
    def from_settings(cls, settings):
        """
        1、@classmethod声明一个类方法，而对于平常我们见到的叫做实例方法。
        2、类方法的第一个参数cls（class的缩写，指这个类本身），而实例方法的第一个参数是self，表示该类的一个实例
        3、可以通过类来调用，就像C.f()，相当于java中的静态方法
        :param settings:
        :return:
        """

        dbparams = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',                     # 编码要加上，否则可能出现中文乱码问题
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=False,
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbparams)
        # 相当于dbpool付给了这个类，self中可以得到
        return cls(dbpool)


    def process_item(self, item, spider):
        """
        pipeline默认调用
        其中的process_item方法是必须调用的用来处理item，并且返回值必须为Item类的对象，或者是抛出DropItem异常
        :param item:
        :param spider:
        :return: Item类的对象
        """
        # line = json.dumps(dict(item)) + '\n'
        # print line
        # self.file.write(line.decode("unicode_escape"))
        # return item
        query = self.dbpool.runInteraction(self._conditional_insert, item)
        query.addErrback(self._handle_error, item, spider)  # 调用异常处理方法
        return item

    def _conditional_insert(self, tx, item):
        """
        写入数据库
        :param tx:
        :param item:
        :return:
        """
        sql = "insert into Deals(date, code, name, price, num, totalPrice, buyer, seller, type) values(%s, %s, %s, %s,  \
              %s, %s, %s, %s, %s)"
        params = (
            item['date'], item['code'], item['name'], item['price'], item['num'], item['totalPrice'], item['buyer'],
            item['seller'], item['type'])
        tx.execute(sql, params)

    def _handle_error(self, failer, item, spider):
        logging.error("mysql_error: " + str( failer))

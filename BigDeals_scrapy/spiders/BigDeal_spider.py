# -*- coding: utf-8 -*-

import scrapy
import logging
import time
from BigDeals_scrapy.items import BigdealsScrapyItem


class BigDealSpider(scrapy.Spider):
    name = "BigDeal"
    allowed_domains = ["vip.stock.finance.sina.com.cn"]
    # 爬取入口
    start_urls = [
        'http://vip.stock.finance.sina.com.cn/q/go.php/vInvestConsult/kind/dzjy/index.phtml'
    ]
    link_extract = {
        'page': ''
    }
    _x_query = {
        'date': 'td[1]/text()',
        'code': 'td[2]/a/text()',
        'name': 'td[3]/a/text()',
        'price': 'td[4]/text()',
        'num': 'td[5]/text()',
        'totalPrice': 'td[6]/text()',
        'buyer': 'td[7]/text()',
        'seller': 'td[8]/text()',
        'type': 'td[9]/text()',
    }

    def parse(self, response):
        """
        parse 负责处理response并返回处理的数据以及(/或)跟进的URL。 Spider 对其他的Request的回调函数也有相同的要求。
        :param response:
        :return:
        """
        # 抓取整个网页
        # return self.crawl_all_pages()

        # 抓取当天的交易数据
        return self.crawl_today_pages()

    # 抓取今天的交易数据
    def crawl_today_pages(self):
        """
        获取今天的时间,比如是"2017-03-31", 爬取前三页的数据,如果时间是"2017-03-31", 则插入数据
        :return:
        """
        # 测试
        today_date = '2017-03-31'
        # today_date = time.strftime('%Y-%m-%d', time.localtime())
        pages_num = 2 + 1
        for i in range(1, pages_num):
            # meta (dict) – the initial values for the Request.meta attribute.
            # If given, the dict passed in this parameter will be shallow copied.
            link_url = 'http://vip.stock.finance.sina.com.cn/q/go.php/vInvestConsult/kind/dzjy/index.phtml?p=' + str(i)
            yield scrapy.Request(url=link_url, meta={'today_time': today_date}, callback=self.parse_page)

    # 抓取整个网页
    def crawl_all_pages(self):
        # http://vip.stock.finance.sina.com.cn/q/go.php/vInvestConsult/kind/dzjy/index.phtml?p=1895
        # 可见网页至多就1895个,那么最简单的办法就是迭代的对1895个网页爬取
        # TODO 这个pages_num需要查看网页进行修改
        pages_num = 1895 + 1
        for i in range(1, pages_num):
            link_url = 'http://vip.stock.finance.sina.com.cn/q/go.php/vInvestConsult/kind/dzjy/index.phtml?p=' + str(i)
            yield scrapy.Request(url=link_url, callback=self.parse_page)

    def parse_page(self, response):

        today_time = response.meta.get("today_time", None)
        trs = response.xpath('//div[@id="divContainer"]/table/tr')
        # logging.info("trs:" + str(trs))
        # 获取下一页地址
        # next_page = response.xpath('//div[@class="pages"]/a[last()]/@onclick').extract()[0]
        # logging.info("next_page:" + next_page)
        items = []
        for tr in trs:
            item = BigdealsScrapyItem()
            # 交易时间
            item['date'] = tr.xpath(self._x_query['date']).extract()[0]
            # 股票代码
            item['code'] = tr.xpath(self._x_query['code']).extract()[0]
            # 股票简称
            item['name'] = tr.xpath(self._x_query['name']).extract()[0]
            # 当前交易价格
            item['price'] = tr.xpath(self._x_query['price']).extract()[0]
            # 成交数量
            item['num'] = tr.xpath(self._x_query['num']).extract()[0]
            # 总成交金额
            item['totalPrice'] = tr.xpath(self._x_query['totalPrice']).extract()[0]
            # 买方
            item['buyer'] = tr.xpath(self._x_query['buyer']).extract()[0]
            # 卖方
            item['seller'] = tr.xpath(self._x_query['seller']).extract()[0]
            # 证券类型
            item['type'] = tr.xpath(self._x_query['type']).extract()[0]

            if today_time is not None:
                if today_time == item['date']:
                    items.append(item)
            else:
                items.append(item)
        # logging.info("load_item: " + str(BigdealItem_loader.load_item()["name"]))
        return items

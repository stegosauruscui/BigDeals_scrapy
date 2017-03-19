# -*- coding: utf-8 -*-

import scrapy

class BigDealSpider(scrapy.Spider):
    name = "BigDeal"
    start_urls = ['http://vip.stock.finance.sina.com.cn/q/go.php/vInvestConsult/kind/dzjy/index.phtml']
    allowed_domains = ["http://vip.stock.finance.sina.com.cn/"]

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        #sites = hxs.path('//fieldset/ul/li')
        print hxs

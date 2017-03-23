# -*- coding: utf-8 -*-

import scrapy
from scrapy.selector import Selector
from BigDeals_scrapy.items import BigdealsScrapyItem


class BigDealSpider(scrapy.Spider):
    name = "BigDeal"
    # 爬取入口
    start_urls = ['http://vip.stock.finance.sina.com.cn/q/go.php/vInvestConsult/kind/dzjy/index.phtml']
    allowed_domains = ["http://vip.stock.finance.sina.com.cn/"]

    def parse(self, response):
        # hxs = HtmlXPathSelector(response)
        # sites = hxs.path('//fieldset/ul/li')
        # print hxs

        sel = Selector(response)
        trs = sel.xpath('//div[@id="divContainer"]/table/tbody/tr')
        items = []
        for tr in trs:
            # 交易时间
            date = tr.xpath("td[1]/text()").extract()
            # 股票代码
            code = tr.xpath("td[2]/text()").extract()
            # 股票简称
            name = tr.xpath("td[3]/text()").extract()
            # 当前交易价格
            price = tr.xpath("td[4]/text()").extract()
            # 成交数量
            num = tr.xpath("td[5]/text()").extract()
            # 总成交金额
            totalPrice = tr.xpath("td[6]/text()").extract()
            # 买方
            buyer = tr.xpath("td[7]/text()").extract()
            # 卖方
            seller = tr.xpath("td[8]/text()").extract()
            # 证券类型
            type = tr.xpath("td[9]/text()").extract()

            item = BigdealsScrapyItem()
            item["date"] = date
            item["code"] = code
            item["name"] = name
            item["price"] = price
            item["num"] = num
            item["totalPrice"] = totalPrice
            item["buyer"] = buyer
            item["seller"] = seller
            item["type"] = type
            items.append(item)
        return items

# -*- coding: utf-8 -*-
from urllib.parse import urlencode
from scrapy import Spider, Request
import scrapy
import json
from stock.items import DataItem


class MoneySpider(scrapy.Spider):
    name = 'money'
    allowed_domains = ['data.eastmoney.com']
    start_urls = ['http://data.eastmoney.com/']

    def start_requests(self):
        data = {'pagesize': '50'}
        base_url = 'http://data.eastmoney.com/DataCenter_V3/gdhs/GetList.ashx?'
        for page in range(1, self.settings.get('MAX_PAGE') + 1):
            data['page'] = page
            params = urlencode(data)
            url = base_url +params
            yield Request(url, self.parse)




    def parse(self, response):
        result = json.loads(response.text)
        for info in result.get('data'):
            item = DataItem()
            item['id'] = info.get('SecurityCode')
            item['name'] = info.get('SecurityName')
            item['price'] = info.get('LatestPrice')
            item['holdernum'] = info.get('HolderNum')
            item['previousnum'] = info.get('PreviousHolderNum')
            item['hasq'] = info.get('HolderAvgStockQuantity')
            yield item




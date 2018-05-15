# -*- coding: utf-8 -*-
import scrapy
from maotaipy3.items import Maotaipy3Item


class Maotai3Spider(scrapy.Spider):
    name = 'maotai3'
    allowed_domains = ['jisilu.cn']
    start_urls = ['http://www.jisilu.cn/data/stock/600519']

    def parse(self, response):
        subselector = response.xpath('//body')  # //script[@type="text/javascript"]')
        # print subselector
        '''
        i = 0
        for subs in subselector.extract():
            if i == 2:
                # sub = subselector.xpath('[@var="__date"]').extract()
                print 1
                item = MaotaiItem()
                item['txt'] = subselector.extract()
                items = []
                items.append(item)
                # items.append(sub)
                return items
            i += 1

        '''
        items = []
        item1 = Maotaipy3Item()
        item1['txt'] = subselector.extract()
        items.append(item1)
        item = Maotaipy3Item()
        item['txt'] = subselector[0].xpath('./script[@type="text/javascript"]').extract()
        items.append(item)
        return items

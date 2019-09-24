# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import scrapy


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        for quote in response.xpath('//div[@class="quote"]'):
            yield {
                'author': quote.xpath('.//small[@class="author"]/text()').extract_first(),
                'text': quote.xpath('normalize-space(./span[@class="text"])').extract_first()
            }
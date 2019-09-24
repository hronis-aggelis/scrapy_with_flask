import logging
#logging.getLogger('scrapy').setLevel(logging.WARNING)
import time
import json
import scrapy
from scrapy.item import Item, Field
#from scrapy_splash import SplashRequest
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
class spider1(scrapy.Spider):
    name = 'corte_ingles_spider'
    #handle_httpstatus_list = [404, 302]
    ###start_urls = ['https://www.elcorteingles.es/moda/A30716945-abrigo-de-mujer-lana-cocida-bolsillos-laterales/']
    start_urls = ['']
    ##custom_settings = {
     #specifies exported fields and order
    ##'FEED_EXPORT_FIELDS': ["site", "number_of_results"],
  ##}

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, self.parse)
            
    
    def parse(self,response):
        item=product_info()
        item['product_id'] = response.xpath('//span[@id="sku-ref"]/@data-sku').extract_first()
        item['title'] = response.xpath('//h2[@class="title"]/text()').extract_first()
        item['brand_name'] = response.xpath('//h2[@itemprop="brand"]//a/text()').extract_first()
        item['category_levels'] = response.xpath('//ul[@id="breadcrumbs"]//li//a//span/text()').extract()
        item['currency'] = response.xpath('//span[@itemprop="priceCurrency"]/text()').extract_first()
        item['price'] = response.xpath('//span[@itemprop="price"]/text()').extract_first()
        item['description'] = response.xpath('//div[@class="description-container"]/p/text()').extract()
        item['image_urls'] = response.xpath('//ul[@class="alternate-images"]//img/@data-screen-src').extract()
        item['google_product_category'] = 1
        item['google_category_id'] = 1
        yield item
        

     
    


class product_info(scrapy.Item):
    product_id = scrapy.Field()
    title = scrapy.Field()
    brand_name = scrapy.Field()
    category_levels = scrapy.Field()
    currency = scrapy.Field()
    price = scrapy.Field()
    description = scrapy.Field()
    image_urls = scrapy.Field()
    google_product_category = scrapy.Field()
    google_category_id = scrapy.Field()
    

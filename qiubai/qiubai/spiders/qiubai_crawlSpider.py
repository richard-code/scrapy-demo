# -*- coding: utf-8 -*-

import scrapy
from items import QiubaiItem
from scrapy.http import Request
from scrapy.spider import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class QiuBaiCrawlSpider(CrawlSpider):
    name = "qiubai_crawlSpider"
    start_urls = [
        "http://www.qiushibaike.com",
    ]

    rules = [
        Rule(LinkExtractor(allow="/article/*")),
        Rule(LinkExtractor(allow="/users/*"), callback="parse_name")
    ]

    def parse_name(self, response):
        print response.xpath("//div[@class='user-header-cover']/h2/text()").extract()[0]


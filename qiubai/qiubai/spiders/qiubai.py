# -*- coding: utf-8 -*-

import scrapy
from items import QiubaiItem
from scrapy.http import Request


class QiuBaiSpider(scrapy.Spider):
    name = "qiubai"
    start_urls = [
        "http://www.qiushibaike.com",
    ]

    # def parse(self, response):
    #     for ele in response.xpath('//div[@class="article block untagged mb15"]'):
    #         authors = ele.xpath('./div[@class="author clearfix"]/a[2]/h2/text()').extract()
    #         contents = ele.xpath('./div[@class="content"]/text()').extract()
    #         yield QiubaiItem(author = authors, content = contents)

    def parse(self, response):
        for href in response.xpath('//span[@class="stats-comments"]/a/@href').extract():
            detail_url = response.urljoin(href)
            req = Request(detail_url, self.parse_detail_upage)
            item = QiubaiItem()
            req.meta["item"] = item
            yield req

    def parse_detail_upage(self, response):
        item = response.meta["item"]
        item["author"] = response.xpath('//div[@class="author clearfix"]/a[2]/h2/text()').extract()[0] if response.xpath('//div[@class="author clearfix"]').extract() else ""
        item["content"] = response.xpath('//div[@class="content"]/text()').extract()[0]
        comments = []
        for comment in response.xpath('//div[starts-with(@class, "comment-block clearfix floor")]'):
            comment_author = comment.xpath('./div[2]/a/text()').extract()[0]
            comment_content = comment.xpath('./div[2]/span/text()').extract()[0]
            comments.append({"comment_author":comment_author, "comment_content":comment_content})
        item["comments"] = comments
        yield item


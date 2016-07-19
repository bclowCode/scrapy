# -*- coding: utf-8 -*-
import scrapy
from myproject.items import MyprojectItem


class BcspiderSpider(scrapy.Spider):
    name = "bcSpider"
    custom_setting = {
            'ROBOTSTXT_OBEY': False
            }

    allowed_domains = ["dmoz.org"]
    start_urls = [
        #"http://www.dmoz.org/Computers/Programming/Languages/Python/Books/",
        #"http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/"
        "http://www.dmoz.org/Computers/Programming/Languages/Python/"
    ]

    def parse(self, response):
        #for href in response.css("ul.directory.dir-col > li > a::attr('href')"):
        for href in response.css("div.cat-item > a"):
            url = response.urljoin(href.xpath('@href').extract_first())
            request = scrapy.Request(url, callback=self.parse_dir_contents)
            request.meta['proxy'] = 'http://127.0.0.1:3128'
            yield request

    def parse_dir_contents(self, response):
        imgUrl = None
        for sel in response.css("div.custom-mozzie"): 
            imgUrl = response.urljoin(sel.xpath('img/@src').extract_first())
             
        for sel in response.css("div.title-and-desc"):
            item = MyprojectItem()
            item['title'] = sel.xpath('a/div[@class="site-title"]/text()').extract_first()
            item['link'] = sel.xpath('a/@href').extract_first()
            item['desc'] = sel.xpath('div[@class="site-descr "]/text()').extract_first().strip()
            if imgUrl is not None :
                item['image_urls'] = [ imgUrl ]
            yield item

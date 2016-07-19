# -*- coding: utf-8 -*-
import scrapy
from myproject.items import MyprojectItem


class BcspiderSpider(scrapy.Spider):
    name = "bcSpider"

    allowed_domains = ["n9.sitetag.us"]
    start_urls = [
        #"http://www.dmoz.org/Computers/Programming/Languages/Python/Books/",
        #"http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/"
        #"http://www.dmoz.org/Computers/Programming/Languages/Python/"
        "http://n9.sitetag.us:8080/page/www.dmoz.org/Computers/Programming/Languages/Python/"
    ]

    def parse(self, response):
        #for href in response.css("ul.directory.dir-col > li > a::attr('href')"):
        for href in response.css("div.cat-item > a"):
            url = response.urljoin(href.xpath('@href').extract_first())
            yield scrapy.Request(url, callback=self.parse_dir_contents)

    def parse_dir_contents(self, response):
        imgUrl = None
        for sel in response.css("div.custom-mozzie"): 
            imgUrl = response.urljoin(sel.xpath('img/@src').extract_first())
             
        for sel in response.css("div.title-and-desc"):
            item = MyprojectItem()
            item['title'] = sel.xpath('a/div[@class="site-title"]/text()').extract_first()
            item['link'] = sel.xpath('a/@href').extract_first()
            item['desc'] = sel.xpath('div[@class="site-descr "]/text()').extract_first().strip()
            item['referral'] = response.url
            if imgUrl is not None :
                item['image_urls'] = [ imgUrl ]
            yield item

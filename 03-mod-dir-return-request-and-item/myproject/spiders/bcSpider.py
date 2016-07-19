# -*- coding: utf-8 -*-
import scrapy
from myproject.items import MyprojectItem
import copy

def getNodeName(s):
    sarr=s.split("/")
    return sarr[-2]

#    return s[s.rfind("/")+1:]

class BcspiderSpider(scrapy.Spider):
    name = "bcSpider"

    allowed_domains = ["n9.sitetag.us"]
    start_urls = [
        #"http://www.dmoz.org/Computers/Programming/Languages/Python/Books/",
        #"http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/"
        #"http://www.dmoz.org/Computers/Programming/Languages/Python/"

#        "http://n9.sitetag.us:8080/page/www.dmoz.org/Computers/Programming/Languages/Python/"

        "http://n9.sitetag.us:8080/page/www.dmoz.org/Computers/Programming/Languages/Python/Development_Tools/",
        "http://n9.sitetag.us:8080/page/www.dmoz.org/Computers/Programming/Languages/Python/Modules/"
    ]

    METAKEY_SEED = 'feebee.seed'
    METAKEY_REFERRAL_LIST = 'feebee.referralList'
    METAKEY_REFERRAL = 'feebee.referral'
    METAKEY_DEPTH = 'feebee.depth'


    def parse(self, response):
        #for href in response.css("ul.directory.dir-col > li > a::attr('href')"):
        referralMeta={}
        if BcspiderSpider.METAKEY_SEED not in response.meta :
            referralMeta[BcspiderSpider.METAKEY_SEED]          = getNodeName(response.url)
            referralMeta[BcspiderSpider.METAKEY_REFERRAL]      = ""
            referralMeta[BcspiderSpider.METAKEY_REFERRAL_LIST] = [ getNodeName(response.url) ]
            referralMeta[BcspiderSpider.METAKEY_DEPTH]         = 0
            response.meta.update(referralMeta)
        else:
            referralMeta[BcspiderSpider.METAKEY_SEED]          = response.meta[BcspiderSpider.METAKEY_SEED]
            referralMeta[BcspiderSpider.METAKEY_REFERRAL]      = getNodeName(response.url)
            response.meta[BcspiderSpider.METAKEY_REFERRAL_LIST].append(getNodeName(response.url))
            referralMeta[BcspiderSpider.METAKEY_REFERRAL_LIST] = response.meta[BcspiderSpider.METAKEY_REFERRAL_LIST]
            referralMeta[BcspiderSpider.METAKEY_DEPTH]         = response.meta[BcspiderSpider.METAKEY_DEPTH] + 1
        self.logger.info('%s depth_tracking: on node [%s], seed [%s], list [%s], depth %d', " " * referralMeta[BcspiderSpider.METAKEY_DEPTH], response.url, referralMeta[BcspiderSpider.METAKEY_SEED], "> ".join(referralMeta[BcspiderSpider.METAKEY_REFERRAL_LIST]), referralMeta[BcspiderSpider.METAKEY_DEPTH])



        for href in response.css("div.cat-item > a"):
            url = response.urljoin(href.xpath('@href').extract_first())
            self.logger.info('    new_request: %s', url)
            request = scrapy.Request(url, callback=self.parse)
            request.meta.update(copy.deepcopy(referralMeta))
            yield request

        for item in self.parse_dir_contents(response):
            yield item
            

    def parse_dir_contents(self, response):
        imgUrl = None
        for sel in response.css("div.custom-mozzie"): 
            imgUrl = response.urljoin(sel.xpath('img/@src').extract_first())
             
        for sel in response.css("div.title-and-desc"):
            item = MyprojectItem()
            item['title']           = sel.xpath('a/div[@class="site-title"]/text()').extract_first()
            item['link']            = sel.xpath('a/@href').extract_first()
            item['desc']            = sel.xpath('div[@class="site-descr "]/text()').extract_first().strip()
            item['referral']        = response.url
            item['referralPath']    = "> ".join(response.meta[BcspiderSpider.METAKEY_REFERRAL_LIST])
            item['seed']            = response.meta[BcspiderSpider.METAKEY_SEED];
            item['depth']           = response.meta[BcspiderSpider.METAKEY_DEPTH];
            if imgUrl is not None :
                item['image_urls'] = [ imgUrl ]
            self.logger.info('new item: %s', item['title'])
            yield item



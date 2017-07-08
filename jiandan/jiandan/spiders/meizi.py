# -*- coding: utf-8 -*-
import scrapy
from ..items import MeizituItem
from ..pipelines import ImageDownloadPipeline


class MeiziSpider(scrapy.Spider):
    name = "meizi"
    allowed_domains = ["jandan.net"]
    start_urls = ['http://jandan.net/ooxx/']
    image_count = 0

    def parse(self, response):
        if  ImageDownloadPipeline.stop_count > 100:
            print("alread download more than 100 pictures, over")
            return
        image_urls = response.css('img').xpath('@src').extract()
        next_page = response.xpath(
            '//a[contains(@title, "Older Comments")]/@href').extract_first()

        print(next_page)
        #for href in image_urls:
        #    print("the %d image url:%s" % (MeiziSpider.image_count,href))
        #    MeiziSpider.image_count += 1
        yield MeizituItem(image_urls=image_urls)

        yield scrapy.Request(next_page , callback=self.parse)

        pass

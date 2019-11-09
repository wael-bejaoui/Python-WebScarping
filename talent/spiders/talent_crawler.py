# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from talent.items import TalentItem

class TalentCrawlerSpider(CrawlSpider):
    name = 'talent_crawler'
    allowed_domains = ['talents.tn']
    start_urls = ['http://www.talents.tn/offres/technologie-de-l-information/?pagesize=50&sort=newest']

    rules = [
        Rule(LinkExtractor(allow=r'questions\?page=[0-15]&sort=newest'),
             callback='parse_item', follow=True)
    ]

    def parse_item(self, response):
        questions = response.xpath('//div[@class="lister__details cf js-clickable"]')

        for question in questions:
            item = TalentItem()
            item['url'] = "/".join(question.xpath(
                'h3/a[@class="js-clickable-area-link"]/@href'
            ).extract()[0].split('/')[1:-1])
            item['title'] = question.xpath(
                'h3/a[@class="js-clickable-area-link"]/span/text()'
            ).extract()[0]
            item['recruiter'] = question.xpath(
                'ul/li[@class="lister__meta-item lister__meta-item--recruiter"]/text()').extract()[0]
            item['region'] = question.xpath(
                'ul/li[@class="lister__meta-item lister__meta-item--location"]/text()').extract()[0]
            item['description'] = question.xpath(
                'p[@class="lister__description js-clamp-2"]/text()').extract()[0]
            yield item

from scrapy import Spider
from scrapy.selector import Selector

from talent.items import TalentItem

class TalentSpider(Spider):
    name = "talent"
    allowed_domains = ["talents.tn"]
    start_urls = [
        "https://www.talents.tn/offres/technologie-de-l-information/?pagesize=50&sort=newest"
    ]

    def parse(self, response):
        questions = Selector(response).xpath('//div[@class="lister__details cf js-clickable"]')

        for question in questions:
            item = TalentItem()
            item['url'] = "/".join(question.xpath(
                'h3/a[@class="js-clickable-area-link"]/@href'
            ).extract()[0].split('/')[1:-1])
            item['title'] = question.xpath(
                'h3/a[@class="js-clickable-area-link"]/span/text()').extract()[0]
            item['recruiter'] = question.xpath(
                'ul/li[@class="lister__meta-item lister__meta-item--recruiter"]/text()').extract()[0]
            item['region'] = question.xpath(
                'ul/li[@class="lister__meta-item lister__meta-item--location"]/text()').extract()[0]
            item['description'] = question.xpath(
                'p[@class="lister__description js-clamp-2"]/text()').extract()[0]

            yield item

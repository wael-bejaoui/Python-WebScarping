from scrapy.item import Item, Field


class TalentItem(Item):
    title = Field()
    url = Field()
    recruiter = Field()
    region = Field()
    description = Field()
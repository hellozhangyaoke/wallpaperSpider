# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WallpaperspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    img_url = scrapy.Field()

    targets = scrapy.Field()

class MaoyanItem(scrapy.Item):

    tag = scrapy.Field()

    categorie = scrapy.Field()

    date = scrapy.Field()

    meta = scrapy.Field()

    thumb = scrapy.Field()

    large = scrapy.Field()

    cover = scrapy.Field()

    full = scrapy.Field()

    color = scrapy.Field()

    old_id = scrapy.Field()
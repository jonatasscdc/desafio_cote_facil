# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PedidoItem(scrapy.Item):
    # define the fields for your item here like:
    motivo = scrapy.Field()
    itens = scrapy.Field()

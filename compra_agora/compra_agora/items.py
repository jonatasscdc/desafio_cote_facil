# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy 

class ProdutoItem(scrapy.Item):
    descricao = scrapy.Field()
    fabricante = scrapy.Field()
    #imagem = scrapy.Field()

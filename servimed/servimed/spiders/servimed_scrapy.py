import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from items import PedidoItem

class PedidoSpider(CrawlSpider):
    name = 'pedido'
    start_urls =['https://pedidoeletronico.servimed.com.br/']

    def __init__(self, pedido, *args, **kwargs):
        super(PedidoSpider, self).__init__(*args, **kwargs)
        self.pedido = pedido

        self.rules = (
            Rule(LinkExtractor(allow=self.pedido, callback='parse_pedido'),)
        )
    
    def parse(self, response):
        return scrapy.FormRequest.from_response(
        response, 
        formdata = {'usuario':'juliano@farmaprevonline.com.br', 'senha':'a007299A'},
    )

    def parse_pedido(self, response):
        pedido = response.xpath('//div/[@id="detalhes-pedido"]')
        if pedido:
            item = PedidoItem()
            item['motivo'] = pedido.xpath('.//h3/text()').get()
            item['itens'] = []
            for tr in pedido.xpath('.//table/tbody/tr'):
                item['itens'].append({
                    'codigo_produto': tr.xpath('.//td[1]/text()').get(),
                    'descricao': tr.xpath('.//td[2]/text()').get(),
                    'quantidade_faturada': tr.xpath('.//td[3]/text()').get()
                })

                yield item
            else:
                yield {'erro': 'Pedido não encontrado'}

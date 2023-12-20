import scrapy
import nacl.pwhash # importe a lib pynacl para fazer o login

class CompraAgoraSpider(scrapy.Spider):
    name = 'compra_agora_spider'
    start_urls = ['https://www.compra-agora.com/'] # URL inicial do spider

    def parse(self, response):
        # faça o login no website usando o método FormRequest do scrapy
        # use a lib pynacl para criptografar a senha
        password = nacl.pwhash.str(b'85243140') # criptografe a senha
        yield scrapy.FormRequest.from_response(
            response,
            formdata={'username': '04.502.445/0001-20', 'password': password},
            callback=self.after_login
        )

    def after_login(self, response):
        # verifique se o login foi bem sucedido
        if 'Bem-vindo' in response.text:
            # o login foi bem sucedido
            self.logger.info('Login bem sucedido')
            # entre em cada categoria usando o método Request do scrapy
            categories = response.xpath('//li[@class="lista-menu-itens"]/a/') # selecione as categorias usando XPATH
            for category in categories:
                # extraia a URL de cada categoria
                category_url = category.xpath('.//@href').get()
                # envie um pedido para a URL de cada categoria
                yield scrapy.Request(category_url, callback=self.parse_category)
        else:
            # o login falhou
            self.logger.error('Login falhou')

    def parse_category(self, response):
        # raspe os dados de todos os produtos disponíveis na categoria
        products = response.xpath('//a[@class="container-information"]/') # selecione os produtos usando XPATH
        for product in products:
            # crie um item para cada produto
            item = CompraAgoraItem()
            # extraia os dados de cada produto: descrição, fabricante e URL da imagem
            item['description'] = product.xpath('//div[@class="product-title"]/text()').get()
            item['manufacturer'] = product.xpath('//div[@class="logo-marca d-llg-none"]/text()').get()
            #item['image_url'] = product.xpath('.//img/@src').get()
            # retorne o item raspado
            yield item

class CompraAgoraItem(scrapy.Item):
    # defina os campos dos dados que queremos raspar
    description = scrapy.Field()
    manufacturer = scrapy.Field()
    image_url = scrapy.Field()

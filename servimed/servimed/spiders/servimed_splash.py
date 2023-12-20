import scrapy
from items import PedidoItem
from scrapy_splash import SplashRequest

lua_script = """
    function main(splash, args)
        assert(splash:go(args.url))
        assert(splash:wait(1))

        splash:set_viewport_full()


        
        return {
            html=splash:html(),
            url = splash:url(),
            cookies = splash:get_cookies(),
            }
        end
"""

class Servimed(scrapy.Spider):
    # Definindo o nome do spider, que é usado para identificá-lo e chamá-lo viepelo terminal
    name = 'servimed'
    pedido = '511082'

    headers = {
        'Accept':'application/json, text/plain, */*',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'pt-BR,pt;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Sec-Fetch-Dest':'empty',
        'Sec-Fetch-Mode':'cors',
        'Sec-Fetch-Site':'same-site',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0'
    }

    def start_requests(self):
        signin_url = 'https://pedidoeletronico.servimed.com.br/login'
        
        yield SplashRequest(
            url=signin_url,
            endpoint='execute',
            splash_headers=self.headers,
            args={
                'width': '1000',
                'lua_source': lua_script,
                'ua': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
            },
        )
    #Definindo o método __init__, que é o construtor da classe e é chamado quando o spider é criado
    def __init__(self, *args, **kwargs):
        # Chamando o método __init__ da classe pai, que é a classe scrapy.Spider
        super(Servimed, self).__init__(*args, **kwargs)
        # Criando um atributo chamado pedido, que é o argumento que o usuário passou para o script, que é o número do pedido
        self.pedido = '511082'
        # Criando um atributo chamado start_urls, que é uma lista que contém as URLs que o spider vai começar a raspar
        # Nesse caso, a única URL é a do site dos pedidos
        self.start_urls = ['https://pedidoeletronico.servimed.com.br/']
    
    
    # Definindo o método parse_login, que é um método auxiliar do spider e é chamado para processar a resposta da página de login
    def parse(self, response):
        # Verificando se o spider conseguiu fazer o login com sucesso, usando o método xpath do objeto response
        # Se o spider encontrou o elemento que contém o texto "Meus Pedidos", significa que ele está na página de pedidos
        if response.xpath('//a[contains(text(), "Meus Pedidos")]'):
            # Criando uma variável chamada url, que contém a URL da página de pesquisa de pedidos
            # A URL é formada pela URL base do site, mais o caminho da página, mais o número do pedido como parâmetro
            url = 'https://pedidoeletronico.servimed.com.br/pedidos/pesquisar?numero=' + self.pedido
            # Fazendo uma requisição GET para a URL da página de pesquisa de pedidos, usando o método scrapy.Request
            # O parâmetro callback é o método que vai processar a resposta da requisição, que nesse caso é o método parse_detalhes
            yield scrapy.Request(url, callback=self.parse_detalhes)
        # Se o spider não encontrou o elemento que contém o texto "Meus Pedidos", significa que ele não conseguiu fazer o login
        else:
            # Imprimindo uma mensagem de erro no terminal, usando o método log do objeto scrapy
            self.logger.error('Login failed')
            # Retornando None, para indicar que o spider não tem mais nada a fazer
            return None
    
    # Definindo o método parse_detalhes, que é um método auxiliar do spider e é chamado para processar a resposta da página de detalhes do pedido
    def parse_detalhes(self, response):
        # Verificando se o spider encontrou o pedido que o usuário inputou, usando o método xpath do objeto response
        # Se o spider encontrou o elemento que contém o texto "Detalhes do Pedido", significa que ele está na página de detalhes do pedido
        if response.xpath('//h1[contains(text(), "Detalhes do Pedido")]'):
            # Criando um objeto chamado item, que é uma instância da classe PedidoItem, que representa o item que contém o retorno de faturamento do pedido
            item = PedidoItem()
            # Extraindo o valor do motivo do pedido, usando o método xpath do objeto response
            # Usando o método get do objeto selector, que retorna o texto do primeiro elemento que corresponde ao XPath
            # Usando o método strip do objeto str, que remove os espaços em branco do início e do fim do texto
            item['motivo'] = response.xpath('//td[contains(text(), "Motivo")]/following-sibling::td/text()').get().strip()
            # Criando uma lista vazia chamada itens, que vai armazenar os itens do pedido
            itens = []
            # Iterando sobre os elementos que contêm os dados dos itens do pedido, usando o método xpath do objeto response
            # Usando o método getall do objeto selector, que retorna uma lista de textos de todos os elementos que correspondem ao XPath
            for row in response.xpath('//table[@id="tableItens"]/tbody/tr'):
                # Criando um dicionário vazio chamado item, que vai armazenar os dados de um item do pedido
                item = {}
                # Extraindo o valor do código do produto, usando o método xpath do objeto row, que é um objeto selector
                # Usando o método get do objeto selector, que retorna o texto do primeiro elemento que corresponde ao XPath
                # Usando o método strip do objeto str, que remove os espaços em branco do início e do fim do texto
                item['codigo_produto'] = row.xpath('./td[1]/text()').get().strip()
                # Extraindo o valor da descrição do produto, usando o método xpath do objeto row, que é um objeto selector
                # Usando o método get do objeto selector, que retorna o texto do primeiro elemento que corresponde ao XPath
                # Usando o método strip do objeto str, que remove os espaços em branco do início e do fim do texto
                item['descricao'] = row.xpath('./td[2]/text()').get().strip()
                # Extraindo o valor da quantidade faturada do produto, usando o método xpath do objeto row, que é um objeto selector
                # Usando o método get do objeto selector, que retorna o texto do primeiro elemento que corresponde ao XPath
                # Usando o método strip do objeto str, que remove os espaços em branco do início e do fim do texto
                item['quantidade_faturada'] = row.xpath('./td[5]/text()').get().strip()
                # Adicionando o dicionário item à lista itens, usando o método append do objeto list
                itens.append(item)
            # Atribuindo a lista itens ao campo itens do objeto item, que é uma instância da classe PedidoItem
            item['itens'] = itens
            # Retornando o objeto item, para que ele possa ser processado pelos pipelines
            yield item
                # Se o spider não encontrou o elemento que contém o texto "Detalhes do Pedido", significa que ele não encontrou o pedido que o usuário inputou
        else:
            # Imprimindo uma mensagem de erro no terminal, usando o método log do objeto scrapy
            self.log('Pedido not found', level=scrapy.log.ERROR)
            # Retornando None, para indicar que o spider não tem mais nada a fazer
            return None

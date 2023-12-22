# Importar as bibliotecas necessárias
import scrapy
from scrapy_splash import SplashRequest
from ..items import ProdutoItem #Importar a classse ProdutoItem do arquivo items.py

# Definir a classe do spider, que herda de scrapy.Spider
class CompraAgoraSpider(scrapy.Spider):
    # Definir o nome do spider que será usado para executá-lo
    name = "compra_agora_splash"

    # Definir o script lua para o splash
    lua_script = """
    function main(splash, args)
        -- Open the website's homepage
        splash:go("https://www.compra-agora.com/")
        -- Wait for the login button to load
        splash:wait(1)
        -- Click the login button
        local login_button = splash:select('#login-text > div > div.first-label')
        login_button:mouse_click()
        -- Wait for the login form to load
        splash:wait(1)
        -- Input the CNPJ
        local cnpj_input = splash:select('#usuarioCnpj')
        cnpj_input:send_text('04.502.445/0001-20')
        -- Input the password
        local password_input = splash:select('#usuarioSenhaCA')
        password_input:send_text('85243140')
        --Mark the captcha
        local captcha = splash:select('#recaptcha-anchor > div.recaptcha-checkbox-checkmark')
        captcha:mouse_click()
        -- Click the login button
        local login_button = splash:select('#realizar-login')
        login_button:mouse_click()
        -- Wait for the page to load
        splash:wait(10)
        return splash:html()
    end
    """
    # Definir o método que tratará a resposta da primeira URL
    def start_requests(self):
        # Enviar uma requisição para o splash, passando o script lua e um callback para o próximo passo.
        yield SplashRequest("https://www.compra-agora.com/", callback=self.after_login, endpoint="execute", args={"lua_source": self.lua_script})

    # Definir o método que irá tratar a resposta do login
    def after_login(self, response):
        # Verificar se o login foi bem sucedido, procurando pelo nome do usuário na resposta
        if "04.502.445/0001-20" in response.text:
            # Se o login foi bem sucedido, imprimir uma mensagem no console
            self.logger.info("Login realizado com sucesso")

            # Obter as URLs das categorias de produtos no menu lateral
            categorias = response.css("ul.sidebar-menu li a::attr(href)").getall()

            # Para cada URL de categoria, enviar uma requisição para o splash e passar um callback para o próximo passo
            for categoria in categorias:
                yield SplashRequest(categoria, self.parse_categoria, endpoint="execute", args={"lua_source": self.lua_script})
        
        else:
            # Se o login não foi bem sucedido, imprimir uma mensagem de erro no console
            self.logger.error("Login falhou!")

    # Definir o método que irá tratar a resposta de cada categoria
    def parse_categoria(self, response):
        # Obter os dados dos produtos da categoria
        produtos = response.css("table#product-table tbody tr")

        # Para cada produto, extrair os dados de descrição, fabricante e URL da imagem
        for produto in produtos: 
            descricao = produto.css("td:nth-child(2) a::text").get()
            fabricante = produto.css("td:nth-child(3)::text").get()
            imagem = produto.css("td:nth-child(1) img::attr(src)").get()

            item = ProdutoItem(
                descricao=descricao,
                fabricante=fabricante,
                imagem=imagem,
            )

            yield item

        # Verificar se há uma url para a próxima página da categoria, que está em um link com o texto "Próximo"
        proxima_pagina = response.css("a.contains('Ver mais produtos')::attr(href)").get()

        # Se houver uma URL para a próxima página, enviar uma requisição para o splash e passar um callback
        if proxima_pagina:
            yield SplashRequest(proxima_pagina, self.parse_categoria, endpoint="execute", args={"lua_source": self.lua_script})
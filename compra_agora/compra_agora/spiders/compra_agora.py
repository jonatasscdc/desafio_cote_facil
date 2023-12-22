#Importar as bibliotecas necessárias
import scrapy 
import json
import nacl.pwhash #Biblioteca para criptografar a senha do usuário
import base64 #Bibioteca para codificar e decodificar os dados da senha do usuario
from compra_agora.items import ProdutoItem #Importar a classe ProdutoItem do arquivo items.py
#Definir a classe do spider, que herda de scrapy.Spider
class CompraAgoraSpider(scrapy.Spider):
    #Definir o nome do spider que será usado para executá-lo
    name = "compra_agora"

    #Definir a(as) URL(s) iniciais que o spider irá acessar
    start_urls = ["https://www.compra-agora.com/"]

    def __init__(self):
        self.usuario = "04.502.445/0001-20"
        self.senha = "85243140"



    #Definir o método que tratará a resposta da primeira URL
    def parse(self, response):
        

        #Obter o valor do token CSRF do formulário de login 
        token = response.xpath("substring-before(substring-after(//script[contains(., 'csrf_token')]/text(), 'csrf_token = '), ';')").get().strip("' ")

        #criptografar a senha usando o algoritmo argon2id e o salt
        senha_criptografada = nacl.pwhash.argon2id.str(self.senha.encode())

        #Converter a senha criptografada em bytes para base64
        senha_criptografada = base64.b64encode(senha_criptografada)

        #Converter a senha criptografada de bytes para string
        senha_criptografada = senha_criptografada.decode()

        #Definir os headers da requisição em um dicionário
        headers = {
            "authority": "www.compra-agora.com",
            "method": "POST",
            "path": "/cliente/logar",
            "scheme": "https",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "Cache-Control": "no-cache",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Newrelic": "eyJ2IjpbMCwxXSwiZCI6eyJ0eSI6IkJyb3dzZXIiLCJhYyI6IjMwOTcxNjciLCJhcCI6IjExMzQxOTY2MDciLCJpZCI6IjZjOTVhZDdlZTc2MzE3YjciLCJ0ciI6ImUzYTFiYjgwOTkxNGMzNWM0MTQ4NWUwODg2ZGQ4Yjc5IiwidGkiOjE3MDIwNDY5NjAwMDB9fQ==",
            "Origin": "https://www.compra-agora.com",
            "Pragma": "no-cache",
            "Referer": "https://www.compra-agora.com/",
            "Sec-Ch-Ua": "\"Microsoft Edge\";v=\"119\", \"Chromium\";v=\"119\", \"Not?A_Brand\";v=\"24\"",
            "Traceparent": "00-e3a1bb809914c35c41485e0886dd8b79-6c95ad7ee76317b7-01",
            "Tracestate": "3097167@nr=0-1-3097167-1134196607-6c95ad7ee76317b7----1702046960000",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0",
            "X-Requested-With": "XMLHttpRequest"
        }

        formdata = {
            "csrf_token": token, 
            "username": self.usuario, 
            "password": senha_criptografada,
        }

        yield scrapy.FormRequest("https://www.compra-agora.com/" , formdata=formdata, headers=headers, callback=self.after_login)

    #Definir o método que irá tratar a resposta do login
    def after_login(self, response):
        #Verificar se o login foi bem sucedido, procurando pelo nome do usuário na resposta
        if "200" in response.text:
            #Se o login foi bem sucedido, imprimir uma mensagem no console
            self.logger.info("Login realizado com sucesso")

            yield scrapy.Request("https://compra-agora.com", callback=self.parse_home)
        
        else:
            #Se o login não foi bem sucedido, imprimir uma mensagem de erro no console
            self.logger.error("Login falhou!")

    # Adicione um novo método para tratar a resposta da página inicial
    def parse_home(self, response):
        # Extrair as URLs das categorias e salvar em uma lista
        self.categorias_urls = response.xpath('//li[@class="lista-menu-itens"]/a/@href').getall()
        self.logger.info(f"Categorias: {self.categorias_urls}")  # Log the category URLs

        # Iniciar a extração com a primeira categoria
        yield scrapy.Request(response.urljoin(self.categorias_urls[0]), callback=self.parse_categoria, meta={'index': 0})
        yield scrapy.Request(response.urljoin(self.categorias_urls[1]), callback=self.parse_categoria, meta={'index': 2})

    def parse_categoria(self, response):
        # Extrair os links dos produtos na página da categoria
        produtos_urls = response.xpath("//li//a[@class='container-information']/@href").getall()

        # Log the product URLs
        self.logger.info(f"Produtos: {produtos_urls}")

        # Percorrer a lista de URLs dos produtos
        for produto_url in produtos_urls:
            yield scrapy.Request(response.urljoin(produto_url), callback=self.parse_produto)

        # Após extrair todos os produtos de uma categoria, passar para a próxima categoria
        index = response.meta['index'] + 1
        if index < len(self.categorias_urls):
            yield scrapy.Request(response.urljoin(self.categorias_urls[index]), callback=self.parse_categoria, meta={'index': index})

    def parse_produto(self, response):
        self.logger.info(f"Response: {response}")  # Log the response
        descricao = response.xpath('//div[@class="product-title"]/text()').getall()
        fabricante = response.xpath('//div[@class="logo-marca d-llg-none"]/text()').getall()

        item = ProdutoItem(
            descricao=descricao,
            fabricante=fabricante,
        )

        yield item

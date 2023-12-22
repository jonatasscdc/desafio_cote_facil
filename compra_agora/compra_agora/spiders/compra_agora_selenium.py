# Importar as bibliotecas necessárias
import scrapy
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from scrapy.selector import Selector
import nacl.pwhash #Biblioteca para criptografar a senha do usuário
import base64 #Bibioteca para codificar e decodificar os dados da senha do usuario
from ..items import ProdutoItem #Importar a classse ProdutoItem do arquivo items.py

# Definir a classe do spider, que herda de scrapy.Spider
class CompraAgoraSpider(scrapy.Spider):
    # Definir o nome do spider que será usado para executá-lo
    name = "compra_agora_selenium"

    # Definir o método __init__, que é chamado quando o spider é criado
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        #chrome_options.add_argument("--headless")
        chrome_options.add_argument("--Allow-running-insecure-content")
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument("--ignore-urlfetcher-cert-requests")
        chrome_options.add_argument("--ignore-ssl-errors")
        chrome_options.add_argument("--ignore-certificate-errors-spki-list")
        chrome_options.add_argument("--Access-Control-Allow-Origin=*")
        #self.driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=chrome_options)
        service = Service(executable_path=ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options = chrome_options)
        #Maximizar a janela
        self.driver.maximize_window()
        #Definir o zoom para 50%
        self.driver.execute_script("document.body.style.zoom='50%'")
    
    # Definir o método que tratará a resposta da primeira URL
    def start_requests(self):
        # Abrir a página inicial do site no navegador
        self.driver.get("https://www.compra-agora.com/")
        self.driver.implicitly_wait(5)
        # Clicar no botão de login
        #Encontrar o botão de login pelo CSS Selector
        login_button = self.driver.find_element(By.XPATH, '//*[@id="login-text"]/div')
        login_button.click()

        # Aguardar o formulário de login carregar
        self.driver.implicitly_wait(10) # Esperar até 10 segundos

        # Obter os dados de login do usuário
        usuario = "04.502.445/0001-20" #CNPJ da empresa
        senha = "85243140"

        # Obter o valor do token CSRF do formulário de login 
        #token  = self.driver.find_element(By.XPATH, '//*[@id="main-header-div"]/script[6]/text()').get_attribute("csrf_token")

        # Obter o valor do salt da senha do formulário de login
        #salt = self.driver.find_element_by_css_selector("input[name=salt]").get_attribute("value")

        # criptografar a senha usando o algoritmo argon2id e o salt
        #senha_criptografada = nacl.pwhash.argon2id.str(senha.encode())

        # Converter a senha criptografada em bytes para base64
        #senha_criptografada = base64.b64encode(senha_criptografada)

        # Converter a senha criptografada de bytes para string
        #senha_criptografada = senha_criptografada.decode()

        # Encontrar e preencher os campos do formulário de login
        campo_usuario = self.driver.find_element(By.XPATH, '/html/body/div[3]/div[1]/div[14]/div/div/div/div[2]/div[1]/form/dl[1]/dd/input')
        campo_usuario.send_keys(usuario)
        campo_senha = self.driver.find_element(By.XPATH, '/html/body/div[3]/div[1]/div[14]/div/div/div/div[2]/div[1]/form/dl[2]/dd/input')
        campo_senha.send_keys(senha)

        #Encontrar o recaptcha
        recaptcha = self.driver.find_element(By.XPATH, '/html/body/div[2]/div[3]/div[1]/div/div/span/div[1]')
        recaptcha.click()

        # Clicar no botão de entrar
        botao_entrar = self.driver.find_element(By.XPATH, '/html/body/div[3]/div[1]/div[14]/div/div/div/div[2]/div[1]/form/p[2]/a')
        botao_entrar.click()

        # Obter o código HTML da página atual
        html = self.driver.page_source

        # Passar o HTML para o Scrapy usando o método scrapy.Selector
        response = Selector(text=html)

        # Chamar o callback para o próximo passo
        yield from self.after_login(response)

    # Definir o método que irá tratar a resposta do login
    def after_login(self, response):
        # Verificar se o login foi bem sucedido, procurando pelo nome do usuário na resposta
        if "04.502.445/0001-20" in response.text:
            # Se o login foi bem sucedido, imprimir uma mensagem no console
            self.logger("Login realizado com sucesso")

            # Obter as URLs das categorias de produtos no menu lateral
            categorias = response.css("ul.sidebar-menu li a::attr(href)").getall()

            # Para cada URL de categoria, enviar uma requisição GET e passar um callback para o próximo passo
            for categoria in categorias:
                yield scrapy.Request(categoria, callback=self.parse_categoria)
        
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


        # Se houver uma URL para a próxima página, enviar uma requisição GET e passar um callback
        if proxima_pagina:
            yield scrapy.Request(proxima_pagina, callback=self.parse_categoria)

        # Fechar o navegador
        self.driver.close()

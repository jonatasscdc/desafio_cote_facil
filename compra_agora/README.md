# Spider Compra Agora

Este projeto é um spider feito com Scrapy, um framework Python para web scraping. O spider raspa dados do site [Compra Agora](https://www.compra-agora.com/), um e-commerce para atacadistas e pequenos comerciantes.

## Objetivo

O objetivo deste projeto é coletar informações sobre os produtos vendidos no site Compra Agora, como nome, preço, categoria, descrição, etc. Esses dados podem ser usados para análise de mercado, comparação de preços, monitoramento de estoque, etc.

## Funcionamento

O spider funciona da seguinte maneira:

- Ele começa pela página inicial do site e extrai os links das categorias de produtos.
- Para cada categoria, ele acessa a página correspondente e extrai os links dos produtos.
- Para cada produto, ele acessa a página de detalhes e extrai as informações desejadas.
- Ele salva os dados em um arquivo JSON.

## Requisitos

Para executar este projeto, você precisa ter o Python 3 e o Scrapy instalados em seu ambiente. Você pode instalar o Scrapy utilizando o seguinte comando `pip install scrapy`, ou, alternativamente, `pip3 install scrapy`.

## Uso
Para usar este projeto, você precisa clonar o repositório em sua máquina e navegar até a pasta do projeto. Em seguida, você pode executar o spider com o seguinte comando:

```scrapy crawl compra_agora -o output.json```

Onde `compra_agora` é o nome do spider, `-o` é a opção para especificar o arquivo de saída, e `output.json` é o nome do arquivo de saída. Você pode alterar o formato do arquivo de saída para CSV ou XML, se preferir.

## Arquivos
Este projeto contém os seguintes arquivos:

`README.md`: Este arquivo, que apresenta o projeto e explica como usá-lo.

`scrapy.cfg`: O arquivo de configuração do Scrapy, que define as configurações globais do projeto.

`compra_agora/`: A pasta que contém o código do spider e os itens.

`__init__.py`: O arquivo que inicializa o pacote do projeto.

`items.py`: O arquivo que define a classe CompraAgoraItem, que representa um item raspado do site.

`middlewares.py`: O arquivo que define os middlewares do projeto, que são componentes que processam as requisições e as respostas do spider.

`pipelines.py`: O arquivo que define os pipelines do projeto, que são componentes que processam os itens raspados pelo spider.

`settings.py`: O arquivo que define as configurações específicas do projeto, como o nome do spider, o user-agent, o limite de requisições, etc.

`spiders/`: A pasta que contém o código do spider.

`__init__.py`: O arquivo que inicializa o pacote dos spiders.

`compra_agora.py`: O arquivo que define a classe CompraAgoraSpider, que é o spider responsável por raspar os dados do site.

##Contribuições

Contribuições são bem-vindas! Se você tem alguma sugestão, correção ou melhoria para o projeto, sinta-se à vontade para fazer um fork do repositório e enviar um pull request.

##Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

Autor
Este projeto foi desenvolvido por mim, jonatasscdc.

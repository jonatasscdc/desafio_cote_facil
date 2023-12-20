# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


#Importando o módulo json
import json
from itemadapter import ItemAdapter

#Definindo a classe JsonPipeline, que implementa um pipeline que armazena os itens em um arquivo JSON
class JsonPipeline(object):
    #Definindo o método open_spider que é chamado quando o spider é aberto
    def open_spider(self, spider):
        #Criando um atributo chamado file, que é um objeto que representa o arquivo JSON que vai armazenar os itens
        #O nome do arquivo é o mesmo do argumento que o usuário passou para o script, que é o número do pedido
        #O modo de abertura do arquivo é "w", que significa escrita
        self.file = open(spider.pedido + '.json', 'w')

    #Definindo o método close_spider, que é chamado quando o spider é fechado
    def close_spider(self, spider):
        #Fechando o arquivo JSON
        self.file.close()

    #Definindo o método process_item, que é chamado para cada item que o spider extrai
    def process_item(self, item, spider):
        #Convertendo o item em um dicionário Python, usando o método asdict do módulo scrapy.utils.serialize
        #Isso é necessário para poder usar o módulo json, que só aceita objetos Python nativos
        item = ItemAdapter.asdict(item)
        #Convertendo o dicionário em uma string JSON, usando o método dumps do módulo JSON
        line = json.dumps(item, indent = 4) + '\n'
        #O parâmetro indent=4 é usado para formatar a string JSON de forma mais legível, com 4 espaços de identação
        #Escrevendo a string JSON no arquivo JSON, usando o método write do objeto file
        self.file.write(line)
        #Retornando o item para que ele possa ser processado por outros pipelines
        return item



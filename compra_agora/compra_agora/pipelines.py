# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json


class CompraAgoraPipeline:

    #Definir o método que será chamado quando o spider for aberto
    def open_spider(self, spider):
        #Abrir um arquivo para a escrita com o nome produtos.json
        self.file = open("produtos.json", "w")

        #Escrever o caractere "[" no arquivo, para iniciar uma lista JSON
        self.file.write("[")

    #Definir o método que será chamado para cada item gerado pelo spider
    def process_item(self, item, spider):

        #Converter o item em uma string JSON, com indentação de 4 espaços
        line = json.dumps(ItemAdapter(item).asdict()) + ",\n"

        #Escrever a string JSON no arquivo, seguida de uma vírgula
        self.file.write(line)
        
        #Retornar o item sem alterações
        return item
    
    def close_spider(self, spider):
        #Escrever o caractere "]" no arquivo, para finalizar a lista JSON
        self.file.write("]")

        #Fechar o arquivo 
        self.file.close()

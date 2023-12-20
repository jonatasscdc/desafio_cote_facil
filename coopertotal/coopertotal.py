# Importando as bibliotecas necessárias
import requests # para fazer requisições HTTP
import json # para manipular dados no formato json
import re # para usar expressões regulares


# Criando uma sessão usando o método requests.Session()
session = requests.Session()

# Fazendo uma requisição GET para a página inicial do site
response = session.get('https://coopertotal.nc7i.app/')

# Verificando o status da resposta
if response.status_code == 200:
    print('Requisição bem sucedida.')
else:
    print('Ocorreu um erro na requisição.')

# Verificando os cookies criados
print('Os cookies criados são:')
print(response.cookies)

# Fazendo uma requisição POST para a página de login do site
response = session.post('https://coopertotal.nc7i.app/index.php?route=account/login', data={'email': 'leonardo@coopertotal.com.br', 'password': '1234'})

# Verificando se o login foi bem sucedido
if response.url == 'http://coopertotal.nc7i.app/':
    print('Login bem sucedido.')
else:
    print('Ocorreu um erro no login.')

# Verificando se o cookie de sessão foi criado
print('O cookie de sessão criado é:')
print(response.cookies['OCSESSID'])

# Fazendo uma requisição GET para a página de pedidos do site
response = session.get('http://coopertotal.nc7i.app/pedido')

#Assegurando que sempre haverá um valore de token, mesmo que seja none
token = None
# Extraindo o token de segurança usando o método response.text e o método re.search
match = re.search(r'name="_token" value="(.+?)"', response.text)
if match:
    token = match.group(1)
    print('O token de segurança é:')
    print(token)
else:
    print('Não foi possível extrair o token de segurança.')

# Fazendo uma requisição POST para a página de criação de pedido do site
response = session.post('http://coopertotal.nc7i.app/pedido/criar', data={'farmacia': '01.621.293/0002-78', 'condicoes': 'CONDICAO DIAMANTE A PRAZO', 'prazo': '42', 'pagamento': 'boleto', '_token': token})

# Verificando se o pedido foi criado
if response.url.startswith('http://coopertotal.nc7i.app/pedido/editar'):
    print('Pedido criado com sucesso.')
else:
    print('Ocorreu um erro ao criar o pedido.')

# Extraindo o número do pedido usando o método response.text e o método re.search
match = re.search(r'name="order_id" value="(.+?)"', response.text)
if match:
    order_id = match.group(1)
    print('O número do pedido é:')
    print(order_id)
else:
    print('Não foi possível extrair o número do pedido.')

# Criando uma lista de tuplas com os códigos de barras e as quantidades dos produtos
items = [(7896241225530, 1), (7897595901927, 2), (7896241225547, 1)]

# Usando um loop for para iterar sobre a lista de tuplas
for barcode, quantity in items:

    # Fazendo uma requisição GET para a página de busca de produtos do site
    response = session.get('http://coopertotal.nc7i.app/produto/buscar', params={'q': barcode})

    # Extraindo o id do produto usando o método response.json() e o operador de indexação
    product_id = response.json()[0]['id']
    print('O id do produto com o código de barras {} é:'.format(barcode))
    print(product_id)

    # Fazendo uma requisição POST para a página de adição de produto ao pedido
    response = session.post('http://coopertotal.nc7i.app/pedido/adicionar', data={'product_id': product_id, 'quantity': quantity, '_token': token})

    # Verificando se o produto foi adicionado
    status = response.json()['status']
    if status == 'success':
        print('Produto adicionado com sucesso.')
    else:
        print('Ocorreu um erro ao adicionar o produto.')

# Fazendo uma requisição GET para a página de edição de pedido
response = session.get('http://coopertotal.nc7i.app/pedido/editar/{}'.format(order_id))

# Extraindo o valor total do pedido usando o método response.text e o método re.search
match = re.search(r'id="total">(.+?)<', response.text)
if match:
    total = match.group(1)
    print('O valor total do pedido é:')
    print(total)

    # Convertendo o valor de texto para um número
    total = float(total.replace(',', '.'))
else:
    print('Não foi possível extrair o valor total do pedido.')

# Verificando se o valor total do pedido é maior ou igual ao valor mínimo para faturamento
if total < 500:
    print('O valor total do pedido é menor que o valor mínimo para faturamento.')

    # Fazendo uma requisição GET para a página de busca de produtos do site
    response = session.get('http://coopertotal.nc7i.app/produto/buscar', params={'q': 7896007547654})

    # Extraindo o id do produto usando o método response.json() e o operador de indexação
    product_id = response.json()[0]['id']
    print('O id do produto com o código de barras 7896007547654 é:')
    print(product_id)

    # Calculando a quantidade mínima necessária para atingir o valor mínimo para faturamento
    min_quantity = (500 - total) / 9.99
    min_quantity = int(min_quantity) + 1
    print('A quantidade mínima necessária para atingir o valor mínimo para faturamento é:')
    print(min_quantity)

    # Fazendo uma requisição POST para a página de adição de produto ao pedido
    response = session.post('http://coopertotal.nc7i.app/pedido/adicionar', data={'product_id': product_id, 'quantity': min_quantity, '_token': token})

    # Verificando se o produto foi adicionado
    status = response.json()['status']
    if status == 'success':
        print('Produto adicionado com sucesso.')
    else:
        print('Ocorreu um erro ao adicionar o produto.')
else:
    print('O valor total do pedido é maior ou igual ao valor mínimo para faturamento.')

# Fazendo uma requisição POST para a página de finalização de pedido
response = session.post('http://coopertotal.nc7i.app/pedido/finalizar', data={'order_id': order_id, '_token': token})

# Verificando se o pedido foi finalizado
status = response.json()['status']
if status == 'success':
    print('Pedido finalizado com sucesso.')
else:
    print('Ocorreu um erro ao finalizar o pedido.')

# Gerando um json com o status e o número do pedido
data = {'status': status, 'order_id': order_id}
json_data = json.dumps(data)
print('O json gerado é:')
print(json_data)
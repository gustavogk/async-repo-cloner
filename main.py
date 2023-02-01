import pika
import json

# Criar uma conexão com o RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# Declarar a fila para enviar mensagens
channel.queue_declare(queue='fila')

# Lista de repositórios para enviar
repos = [
    {'repo_url': 'https://github.com/gustavogk/letmeask.git', 'user_id': 'user1'},
    {'repo_url': 'https://github.com/gustavogk/dashgo.git', 'user_id': 'user2'},
    {'repo_url': 'https://github.com/gustavogk/auth-jwt.git', 'user_id': 'user3'},
    {'repo_url': 'https://github.com/gustavogk/letmeask.git', 'user_id': 'user4'},
    {'repo_url': 'https://github.com/gustavogk/letmeask.git', 'user_id': 'user5'},
]

# Enviar as mensagens
for repo in repos:
    message = json.dumps(repo)
    channel.basic_publish(exchange='',
                          routing_key='fila',
                          body=message)
    print(f'[x] Mensagem enviada: {message}')

# Fechar a conexão
connection.close()
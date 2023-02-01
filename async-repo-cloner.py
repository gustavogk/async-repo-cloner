import pika
import json
import os
import threading
from pydriller import Repository, Git
from git import Repo, GitCommandError

# Criar uma conexão com o RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# Declarar a fila para receber mensagens
channel.queue_declare(queue='fila')

def clone_repo(repo_url, username):
    # Criar a pasta para salvar o repositório
    repo_folder = f'repos/{username}'
    if not os.path.exists(repo_folder):
        os.makedirs(repo_folder)

    # Clonar o repositório usando PyDriller
    Repo.clone_from(repo_url, repo_folder)
    print(f'[x] Repositório clonado para {repo_folder}')

def callback(ch, method, properties, body):
    # Converter a mensagem para dicionário
    message = json.loads(body)

    # Obter a URL do repositório e o nome de usuário
    repo_url = message['repo_url']
    username = message['user_id']

    # Iniciar uma nova thread para clonar o repositório
    t = threading.Thread(target=clone_repo, args=(repo_url, username))
    t.start()

# Configurar o consumidor para receber mensagens
channel.basic_consume(queue='fila',
                      auto_ack=True,
                      on_message_callback=callback)

# Iniciar o loop de consumo
print('[*] Aguardando mensagens. Para sair pressione CTRl+C')
channel.start_consuming()
import pika
import json
import os
import datetime
import threading
import logging
from git import Repo, GitCommandError

now = datetime.datetime.now()

log_file_name = 'logs/async-repo-cloner-{}.log'.format(now.strftime('%d-%m-%Y_%H-%M'))

logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
                    datefmt='%d/%m/%Y %H:%M:%S', filename=log_file_name, 
                    filemode='w',
                    encoding='utf-8'
                    )

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='fila')

def clone_repo(repo_url, username):

    try:
        repository = repo_url.split('/')[4]
        repo_folder = f'repos/{username}/{repository}'
        if not os.path.exists(repo_folder):
            os.makedirs(repo_folder)

        logging.info(f'[START] Iniciando a clonagem do repositório {repo_url}...')
        print(f'[START] Iniciando a clonagem do repositório {repo_url}...')
        start_time = datetime.datetime.now()

        Repo.clone_from(repo_url, repo_folder)

        
        end_time = datetime.datetime.now()
        print(f'[END] Tempo de clonagem do repositório {repo_url}: {end_time - start_time}')
        logging.info(f'[END] Tempo de clonagem do repositório {repo_url}: {end_time - start_time}')

    except Exception as ex:
        logging.error(f'Erro ao clonar repositorio {repo_url}, {str(ex)}')

def callback(ch, method, properties, body):

    try:
    # Converter a mensagem para dicionário
        message = json.loads(body)

        # Obter a URL do repositório e o nome de usuário
        repo_url = message['repo_url']
        username = message['user_id']

        # Iniciar uma nova thread para clonar o repositório
        t = threading.Thread(target=clone_repo, args=(repo_url, username))
        t.start()
    except Exception as ex:
        print(f'Erro na criação da thread')

# Configurar o consumidor para receber mensagens
channel.basic_consume(queue='fila',
                      auto_ack=True,
                      on_message_callback=callback)

# Iniciar o loop de consumo
print('[*] Aguardando mensagens. Para sair pressione CTRl+C')
channel.start_consuming()
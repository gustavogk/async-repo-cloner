import pika
import json
import os
import datetime
import subprocess
import logging
from multiprocessing import Process

now = datetime.datetime.now()

log_file_name = 'logs/cloner/teste5-async-repo-cloner-process-{}.log'.format(now.strftime('%d-%m-%Y'))


connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', heartbeat=0))
channel = connection.channel()

#channel.queue_declare(queue='fila', durable=True)
channel.queue_declare(queue='clone_queue', durable=True)
channel.queue_declare(queue='analysis_queue', durable=True)

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%d/%m/%Y %H:%M:%S',
                    filename=log_file_name,
                    filemode='a',
                    encoding='utf-8'
                        )

def clone_repo(repo_url, username):
    
    try:
        repository = repo_url.split('/')[4]
        repo_folder = f'repos/{username}/{repository}'
        if not os.path.exists(repo_folder):
            os.makedirs(repo_folder)

        logging.info(f'[START] Iniciando a clonagem do repositório {repo_url}...')
        print(f'[START] Iniciando a clonagem do repositório {repo_url}...')
        start_time = datetime.datetime.now()

        subprocess.check_output(['git','clone', repo_url, repo_folder])

        end_time = datetime.datetime.now()
        print(f'[END] Tempo de clonagem do repositório {repo_url}: {end_time - start_time}')
        logging.info(f'[END] Tempo de clonagem do repositório {repo_url}: {end_time - start_time}')

        try:
            
            repo_path = {'repo_path': os.path.abspath(repo_folder)}
            message = json.dumps(repo_path)
            channel.basic_publish(exchange='',
                                  routing_key='analysis_queue',
                                  body=message)
            print(f'[x] Mensagem enviada: {message}')

        except Exception as ex:
            logging.error(f'Erro ao enviar caminho do repositorio {repo_url}, {str(ex)}')

    except Exception as ex:
        logging.error(f'Erro ao clonar repositorio {repo_url}, {str(ex)}')
        
def callback(ch, method, properties, body):
    try:
        # Converter a mensagem para dicionário
        message = json.loads(body)

        # Obter a URL do repositório e o nome de usuário
        repo_url = message['repo_url']
        username = message['user_id']

        clone_process = Process(target=clone_repo, args=(repo_url, username))
        clone_process.start()

    except Exception as ex:
        print(f'Erro na criação do processo',{str(ex)})

if __name__ ==  '__main__':

    channel.basic_consume(queue='clone_queue',
                      auto_ack=True,
                      on_message_callback=callback)

    # Iniciar o loop de consumo
    print('[*] Aguardando mensagens. Para sair pressione CTRl+C')
    channel.start_consuming()

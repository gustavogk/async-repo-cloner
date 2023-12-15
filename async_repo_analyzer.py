import pika
import json
import os
import shutil
import datetime
import logging
import git
from multiprocessing import Process

now = datetime.datetime.now()

log_file_name = 'logs/analyzer/teste5-async-repo-analyzer-process-{}.log'.format(now.strftime('%d-%m-%Y'))

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%d/%m/%Y %H:%M:%S',
                    filename=log_file_name,
                    filemode='a',
                    encoding='utf-8'
                        )

# Função para contar arquivos em um diretório
def count_files(directory):
    file_count = 0
    for root, dirs, files in os.walk(directory):
        file_count += len(files)
    return file_count

# Função para contar a quantidade de commits em um repositório Git
def count_commits(repo_path):
    repo = git.Repo(repo_path)
    total_commits = len(list(repo.iter_commits()))
    return total_commits

# Função para calcular o tamanho do repositório
def repo_size(repo_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(repo_path):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            total_size += os.path.getsize(filepath)
    return total_size

def analyze_repo(repo_path):
    try:

        logging.info(f'[START] Iniciando a analise do repositório {repo_path}...')
        print(f'[START] Iniciando a analise do repositório {repo_path}...')
        start_time = datetime.datetime.now()

        # Variáveis para armazenar informações
        total_files = count_files(repo_path)
        total_commits = count_commits(repo_path)
        total_size = repo_size(repo_path)

        # Imprime os resultados
        logging.info(f"[INFO] Total de arquivos no repositório: {repo_path}, {total_files}")
        logging.info(f"[INFO] Total de commits no repositório: {repo_path}, {total_commits}")
        logging.info(f"[INFO] Tamanho do repositório: {repo_path}, {total_size / (1024*1024):.2f} MB")

        end_time = datetime.datetime.now()
        print(f'[END] Tempo de analise do repositório {repo_path}: {end_time - start_time}')
        logging.info(f'[END] Tempo de analise do repositório {repo_path}: {end_time - start_time}')
        
    except Exception as ex:
        logging.error(f'Erro ao analisar repositorio {repo_path}, {str(ex)}')


def callback(ch, method, properties, body):
    try:
        # Converter a mensagem para dicionário
        message = json.loads(body)

        # Obter o caminho do repositório
        repo_path = message.get('repo_path')

        if repo_path:
            analyze_process = Process(target=analyze_repo, args=(repo_path,))
            analyze_process.start()
        else:
            logging.warning('Caminho do repositório ausente na mensagem recebida.')

    except Exception as ex:
        print(f'Erro na criação do processo',{str(ex)})

if __name__ ==  '__main__':

    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', heartbeat=0))
    channel = connection.channel()

    channel.queue_declare(queue='analysis_queue', durable=True)

    # Configurar o consumidor para receber mensagens
    channel.basic_consume(queue='analysis_queue',
                      auto_ack=True,
                      on_message_callback=callback)

    # Iniciar o loop de consumo
    print('[*] Aguardando mensagens. Para sair pressione CTRl+C')
    channel.start_consuming()

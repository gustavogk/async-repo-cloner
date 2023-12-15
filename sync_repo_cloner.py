import subprocess
import datetime
import os 
import logging

now = datetime.datetime.now()

log_file_name = 'logs/sync/sync_repo_cloner-4-{}.log'.format(now.strftime('%d-%m-%Y'))

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

    except Exception as ex:
        logging.error(f'Erro ao clonar repositorio {repo_url}, {str(ex)}')

if __name__ ==  '__main__':

    # Lista de repositórios (substitua com os seus próprios)
    repos = [
        {'repo_url': 'https://github.com/apache/accumulo.git', 'user_id': 'user1'},
        {'repo_url': 'https://github.com/apache/calcite.git', 'user_id': 'user2'},
        {'repo_url': 'https://github.com/apache/chukwa.git', 'user_id': 'user3'},
        {'repo_url': 'https://github.com/apache/cassandra.git', 'user_id': 'user4'},
        {'repo_url': 'https://github.com/apache/jackrabbit.git', 'user_id': 'user5'},
        {'repo_url': 'https://github.com/FasterXML/jackson.git', 'user_id': 'user6'},
        {'repo_url': 'https://github.com/apache/jspwiki.git', 'user_id': 'user7'},
        {'repo_url': 'https://github.com/square/retrofit.git', 'user_id': 'user8'},
        {'repo_url': 'https://github.com/apache/struts.git', 'user_id': 'user9'},
        {'repo_url': 'https://github.com/apache/jena.git', 'user_id': 'user10'},
        {'repo_url': 'https://github.com/apache/lucene-solr.git', 'user_id': 'user11'},
        {'repo_url': 'https://github.com/apache/ant-ivy.git', 'user_id': 'user12'},
        {'repo_url': 'https://github.com/jenkinsci/jenkins.git', 'user_id': 'user13'},
        {'repo_url': 'https://github.com/SeleniumHQ/selenium.git', 'user_id': 'user14'},
        {'repo_url': 'https://github.com/cbeust/testng.git', 'user_id': 'user15'},
        {'repo_url': 'https://github.com/apache/pdfbox.git', 'user_id': 'user16'},
        {'repo_url': 'https://github.com/apache/poi.git', 'user_id': 'user17'},
        {'repo_url': 'https://github.com/apache/xerces2-j.git', 'user_id': 'user18'},
        {'repo_url': 'https://github.com/apache/druid.git', 'user_id': 'user19'},
        {'repo_url': 'https://github.com/pgjdbc/pgjdbc.git', 'user_id': 'user20'},
        {'repo_url': 'https://github.com/apache/activemq.git', 'user_id': 'user21'},
        {'repo_url': 'https://github.com/apache/mina.git', 'user_id': 'user22'},
        {'repo_url': 'https://github.com/alibaba/fastjson.git', 'user_id': 'user23'},
        {'repo_url': 'https://github.com/google/gson.git', 'user_id': 'user24'},
        {'repo_url': 'https://github.com/google/guava.git', 'user_id': 'user25'},
    ]

    # Loop para clonar cada repositório na lista
    for repo in repos:
        repo_url = repo['repo_url']
        username = repo['user_id']
        clone_repo(repo_url, username)

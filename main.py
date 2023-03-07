import pika
import json

# Criar uma conexão com o RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# Declarar a fila para enviar mensagens
channel.queue_declare(queue='fila')

# Lista de repositórios para enviar
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

# Enviar as mensagens
for repo in repos:
    message = json.dumps(repo)
    channel.basic_publish(exchange='',
                          routing_key='fila',
                          body=message)
    print(f'[x] Mensagem enviada: {message}')

# Fechar a conexão
connection.close()
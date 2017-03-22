import codecs
import json
import os

from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch import helpers

from srv.utils.YAML_Parser import YAML_Parser

exec_path = os.getcwd()
print("Exec Path : " + exec_path)

start_time = datetime.now()
print("Début : " + start_time.strftime('%Y-%m-%d %H:%M:%S'))

# Load config file
#config_file_path = file = exec_path + "\\config\\config.yaml"
config_file_path = os.path.join(exec_path, "config", "config.yaml")
yaml_parser = YAML_Parser(file=config_file_path)

# global config parameters
config = yaml_parser.parse()
elasticsearch_config = config.get("elasticsearch")
elasticsearch_host = elasticsearch_config.get("host")
elasticsearch_port = elasticsearch_config.get("port")
elasticsearch_timeout = elasticsearch_config.get("timeout")
elasticsearch_index = elasticsearch_config.get("index")
elasticsearch_doc_type = elasticsearch_config.get("doc_type")
elasticsearch_settings_fields_limit = elasticsearch_config.get("settings").get("index.mapping.total_fields.limit")
import_file_name = config.get("import_file")

es = Elasticsearch(timeout=elasticsearch_timeout, hosts=elasticsearch_host + ":" + str(elasticsearch_port))
index_name = elasticsearch_index
doc_type_name = elasticsearch_doc_type
path = os.path.join(exec_path, "data", import_file_name)
#path = exec_path + '\\data\\' + import_file_name

settings = {"settings": {"index.mapping.total_fields.limit": elasticsearch_settings_fields_limit}}  #

#Prepare DB, delete index if already exist, and set settings
if es.indices.exists(index=index_name):
    es.indices.delete(index=index_name)
exit()
es.indices.create(index=index_name)
es.indices.put_settings(index=index_name, body=settings)

countRows = 0;


def blocks(files, size=65536):
    while True:
        b = files.read(size)
        if not b: break
        yield b


def format_json(index, type, data):
    return {
        '_op_type': 'index',
        '_index': index,
        '_type': type,
        '_source': data
    }

with codecs.open(path, 'r', 'utf-8') as f:
    countRows = sum(bl.count("\n") for bl in blocks(f))

print("Nombre total de lignes : " + str(countRows))

data = []
i = 0
with codecs.open(path, 'r', 'utf-8') as f:
    for line in f:
        body = format_json(index_name, doc_type_name, json.loads(line) )
        data.append(body)
        i += 1
        if i % 10000 == 0 or i >= countRows:
            helpers.bulk(client=es, actions=data,stats_only=True)
            print( str(i) + "/" + str(countRows) + " (" + str(round(100 * i / countRows)) + "%)" )
            del data[:]



end_time = datetime.now()
print("Fin : " + end_time.strftime('%Y-%m-%d %H:%M:%S'))

turnaround =end_time - start_time
total_seconds = int(turnaround.total_seconds())
hours, remainder = divmod(total_seconds,60*60)
minutes, seconds = divmod(remainder,60)
print('Temps total : {} hrs {} mins {} secs'.format(hours,minutes,seconds))

# -*- coding: utf-8 -*-
import os
import re
from datetime import datetime
import elasticsearch
from flask import Flask, jsonify, request

from utils.Adresse import Adresse
from utils.YAML_Parser import YAML_Parser

exec_path = os.getcwd()
print("Exec Path : " + exec_path)
# Load config file
config_file_path = file = exec_path + "\\config\\config.yaml"
yaml_parser = YAML_Parser(file=config_file_path)


# global config parameters
config = yaml_parser.parse()

srv_config = config.get("server")
srv_host = srv_config.get('host')
srv_port = srv_config.get('port')
srv_debug = srv_config.get('debug')

elasticsearch_config = config.get("elasticsearch")
elasticsearch_host = elasticsearch_config.get("host")
elasticsearch_port = elasticsearch_config.get("port")
elasticsearch_timeout = elasticsearch_config.get("timeout")
elasticsearch_index = elasticsearch_config.get("index")
elasticsearch_doc_type = elasticsearch_config.get("doc_type")
elasticsearch_fuzzy_level = elasticsearch_config.get("fuzzy_level")

type_adresse = config.get("adresse_search").get("type_voie")

print("Elasticsearch running on http://" + elasticsearch_host + ":" + str(elasticsearch_port))

app = Flask(__name__)
es = elasticsearch.Elasticsearch(timeout=elasticsearch_timeout, hosts=elasticsearch_host + ":" + str(elasticsearch_port))
start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def error(msg):
    return {
        "error": msg
    }




def query_adresse(name):
    # fuzzy search on eleasticsearch
    formated_adresse = name.replace(" ", "~ ") + "~"
    print("formated adresse : " + formated_adresse)
    results = es.search(
        index=elasticsearch_index,
        doc_type=elasticsearch_doc_type,
        body={
            "from": 0,
            "size": 10,
            "query": {
                "query_string": {
                    "query": formated_adresse,
                    "fields": [
                        "name",
                        "city",
                        "housenumbers"
                    ],
                    "fuzziness": elasticsearch_fuzzy_level
                }
            }
        }
    )
    return results.get("hits").get("hits")



@app.route("/")
def default():
    return jsonify({
        "start_time": start_time,
        "elasticsearch": es.cluster.health().get("status")
    })


@app.route("/adresse")
def adresse():
    name = request.args.get('name') or ""
    lat = request.args.get('lat') or ""
    lon = request.args.get('lon') or ""

    if name == "":
        return jsonify(error("Parameter `name` must be provided in URL"))
    elif name != "" and lat == "" and lon =="":
        results = query_adresse(name) #Find city and address but not address number
        adresse = Adresse(adresse_str=name,types_adresses=type_adresse,elasticsearch_result=results)
        retour = adresse.list_results_find()
        return jsonify(retour)
    elif name != "" and lat != "" and lon != "":
        results = query_adresse(name)  # Find city and address but not address number
        adresse = Adresse(adresse_str=name, types_adresses=type_adresse, elasticsearch_result=results,latitude=lat,longitude=lon)
        retour = adresse.list_results_find()
        return jsonify(retour)



if __name__ == "__main__":
    app.run(debug=srv_debug, port=srv_port, host=srv_host)

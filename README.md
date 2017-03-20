## Synopsis

L'objectif est de fournir une API simple afin d'améliorer la sélection d'une adresse physique.
L'api reçoit l'adresse rentrée par l'utilisateur, et doit fournir en sortie une liste d'adresse (10 max) possible.
Exemples de formats d'adresse différents:

* 2 Lotissement Le Panoramique 1400 L'Abergement-Clémenciat
* 167 rue Alexandre Bérard, Ambérieu-en-Bugey
* Troyes, 13 rue voltaire

## Code Example

All commands must be run from the current path(config,data,srv,env.py,...)
* config/config.yaml contains configurable parameters
* Run Import Data in Elasticsearch : python env.py
* Run API Server : python srv/index.py

1. Download on https://bano.openstreetmap.fr/data/ file named "full.sjson.gz"
2. Decompress it in the folder "data" with default name "full.sjson" (The file name is configurable in the file config/congi.yaml )
3. Run your elasticsearch server
4. Run command python env.py to import data into elastic search (This may take a long time because of the size of "full.sjson" )
5. Run command python srv/index.py to launch the HTTP Server and querying address

## Requierements

* Python 3.5.*
* Elasticsearch 5.1.*

## API Reference

##### Return infos about http server and elasticsearch server
* GET http://adresse:port/ 
    * return {
"elasticsearch": "state of elasticsearch cluster",
"start_time": "start_time of server"
} 

##### Search an address
* GET http://adresse:port/adresse?name=your adresse
    *  { "house_number_find": "number of results find",
"query": "your input query",
"results": [{
"city": "City Find",
"house_number": "",
"lat": "",
"lon": "",
"name": "",
"postcode": "",
"region": "",
"score": ""
}]}

##### Search an address with coordinates
* GET http://adresse:port/adresse?name=your adresse&lat=your latitude&lon=your longitude
    *  { "house_number_find": "number of results find",
"query": "your input query",
"results": [{
"city": """,
"distance": Distance Between input coordinates and find coordinates",
"house_number": "",
"lat": "",
"lon": "",
"name": "",
"postcode": "",
"region": "",
"score": ""
}]}




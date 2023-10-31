from elasticsearch import Elasticsearch
from pydantic import BaseModel
from lista_entrenamineto import *

es =Elasticsearch(['http://localhost:9200'], basic_auth=('elastic', 'elastic'))

def docEntity(item):
    return{
        "_id": item["_id"],
        "_source": item["_source"]
    }

indexName = "es_train_data"

#creando un indice desde python
#ya esta base de datos fue creada por lo que la comentamos
#es.indices.create(index=indexName,ignore = 400)

#saber si existe un indice
#print(es.indices.exists(index = indexName))



settings = {
    "mappings": {
        "properties": {
            "text": {"type": "text"},
            "entities": {"type": "nested"}
        }
    }
}

#esto se pone solamente si el archivo no ha sido creado antes
es.indices.create(index=indexName, body=settings)

for i, doc in enumerate(documentos.values(), start=1):
    es.index(index=indexName, id=i, document=doc)
    
    
def getPythonzonas():
    docs = es.search(index=indexName, body={"query": {"match_all": {}}}, size=1000)
    return [docEntity(d) for d in docs["hits"]["hits"]]

arr = getPythonzonas()
resultados = []

for el in arr:
    texto = el["_source"]["text"]
    entities = el["_source"]["entities"]
    entities_formatted = [(entity["start"], entity["end"], entity["label"]) for entity in entities]
    resultado = (texto, {"entities": entities_formatted})
    print(resultado)
    resultados.append(resultado)

#print(resultados)

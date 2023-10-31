from elasticsearch import Elasticsearch
#from fastapi import APIRouter
from pydantic import BaseModel

es =Elasticsearch(['http://localhost:9200'], basic_auth=('elastic', 'elastic'))

def docEntity(item):
    return{
        "_id": item["_id"],
        "_source": item["_source"]
    }

indexName = "borrar"

#creando un indice desde python
#ya esta base de datos fue creada por lo que la comentamos
es.indices.create(index=indexName,ignore = 400)

#saber si existe un indice
#print(es.indices.exists(index = "archivo_para_ner"))


doc1 = {
    "text": "Hola mi nombre es Luis y soy de la provincia de Santiago de Cuba",
}

#para crear una tabla y pasarle los datos
#es.index(index='archivo_para_ner',  id=1, document=doc1)
es.index(index=indexName,  id=1, document=doc1)

#para obtener los valores de la tabla
#res = es.get(index='archivo_para_ner' , id=1)
#print(res._body)

res = es.get(index=indexName , id=1)
#print(res)

def getPythonzonas():
    docs = es.search(index=indexName)
    return [docEntity(d) for d in docs["hits"]["hits"]]

arr = getPythonzonas()

text_value = arr[0]["_source"]["text"]
print(text_value)

#borrando in index
es.indices.delete(index = indexName )



from elasticsearch import Elasticsearch

es =Elasticsearch(['http://localhost:9200'], basic_auth=('elastic', 'elastic'))

#saber si estas conectado
#print(es.info())

#creando un indice desde python
#ya esta base de datos fue creada por lo que la comentamos
#es.indices.create(index="borrar",ignore = 400)

#saber si existe un indice
#print(es.indices.exists(index = "archivo_para_ner"))


doc1 = {
    "city": "Santiago de Cuba",
    "country": "Cuba",
}

#para crear una tabla y pasarle los datos
#es.index(index='archivo_para_ner',  id=1, document=doc1)
#es.index(index='borrar',  id=1, document=doc1)

#para obtener los valores de la tabla
#res = es.get(index='archivo_para_ner' , id=1)
#print(res._body)

res = es.get(index='borrar' , id=1)
print(res)

#borrando in index
es.indices.delete(index = "borrar")
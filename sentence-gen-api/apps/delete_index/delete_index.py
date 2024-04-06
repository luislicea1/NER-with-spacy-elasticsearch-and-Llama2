from elasticsearch import Elasticsearch

es =Elasticsearch(['http://localhost:9200'], basic_auth=('elastic', 'elastic'))

indexName1 = "datos_entrenamiento"
indexName2 = "datos_comprobacion"
indexName3 = "datos_sin_etiquetar"
indexName = "users_datys"

# es.indices.delete(index=indexName1, ignore=[400, 404])
# es.indices.delete(index=indexName2, ignore=[400, 404])
# es.indices.delete(index=indexName3, ignore=[400, 404])
es.indices.delete(index=indexName, ignore=[400, 404])
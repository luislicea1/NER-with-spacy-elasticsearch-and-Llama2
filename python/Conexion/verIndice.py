from elasticsearch import Elasticsearch

# Crear una instancia del cliente de Elasticsearch
client = Elasticsearch(['http://localhost:9200'], basic_auth=('elastic', 'elastic'))

# Especificar el índice que se quiere consultar
#index = "es_train_data"
#index = "archivo_para_ner"
#index = "archivo_para_comprobar"
#index = "ar.datasets"

# Realizar la consulta para obtener todos los documentos del índice
result = client.search(index=index, body={"query": {"match_all": {}}}, size=1000)

print(result)
# Imprimir los resultados
#for hit in result.get("hits", {}).get("hits", []):
#    print(hit.get("_source", {}))
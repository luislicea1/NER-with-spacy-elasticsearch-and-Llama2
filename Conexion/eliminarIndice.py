from elasticsearch import Elasticsearch
from pydantic import BaseModel

es =Elasticsearch(['http://localhost:9200'], basic_auth=('elastic', 'elastic'))

indexName = "es_train_data"
#indexName = "archivo_para_comprobar"

es.indices.delete(index=indexName, ignore=[400, 404])
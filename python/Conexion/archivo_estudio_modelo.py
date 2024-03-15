from elasticsearch import Elasticsearch
from pydantic import BaseModel

es =Elasticsearch(['http://localhost:9200'], basic_auth=('elastic', 'elastic'))

indexName = "model_stats"

documentos = {
    "model1": {
        "model_name": "es_core_news_lg",
        "date": "2024-03-14T00:00:00Z",
        "accuracy": 0.0 
    },
}


settings = {
    "mappings": {
        "properties": {
            "model_name": {"type": "text"},
            "date": {"type": "date"}, 
            "accuracy": {"type": "float"}
        }
    }
}

es.indices.create(index=indexName, body=settings)

for i, doc in enumerate(documentos.values(), start=1):
    es.index(index=indexName, id=i, document=doc)
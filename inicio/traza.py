from elasticsearch import Elasticsearch
from datetime import datetime
es =Elasticsearch(['http://localhost:9200'], basic_auth=('elastic', 'elastic'))

indexName = "traza"

settings = {
    "mappings": {
        "properties": {
            "username": {"type": "keyword"},
            "timestamp": {"type": "date"},
            "action_type": {"type": "keyword"}
        }
    }
}

def insert_trace():
    
    current_time = datetime.now().isoformat()
    doc = {
        "username": "user",
        "timestamp": current_time,
        "action_type": "Inicialización del sistema"
    }
    
    
    if not es.indices.exists(index=indexName):
        es.indices.create(index=indexName, body=settings)
    es.index(index=indexName, body=doc)
    
insert_trace()
from elasticsearch import Elasticsearch
from pydantic import BaseModel

es =Elasticsearch(['http://localhost:9200'], basic_auth=('elastic', 'elastic'))
indexName = "data_to_review"
settings = {
    "mappings": {
        "properties": {
            "text": {"type": "text"},
            "entities": {"type": "nested"}
        }
    }
}

def createTableToReview():
     es.indices.create(index=indexName, body=settings)
     
createTableToReview()
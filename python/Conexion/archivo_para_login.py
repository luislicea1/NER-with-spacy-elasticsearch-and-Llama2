from elasticsearch import Elasticsearch
from pydantic import BaseModel

es =Elasticsearch(['http://localhost:9200'], basic_auth=('elastic', 'elastic'))

indexName = "users_datys"

#estos son los datos de comprobacion
documentos = {
    "user1": {
        "username": "admin",
        'password': "admin",
        "rol": "admin",
    },
    "user2": {
        "username": "luis",
        'password': "$2b$12$.QIlN.DplH6r6Z3uRx3AFOCZGtCOdIJQ89eJ5pQ.yz7jd2JypYUne",
        "rol": "user",
    },
    
}


settings = {
    "mappings": {
        "properties": {
            "username": {"type": "text"},
            "password": {"type": "text"},
            "rol": {"type": "text"}
        }
    }
}


#esto se pone solamente si el archivo no ha sido creado antes
es.indices.create(index=indexName, body=settings)

for i, doc in enumerate(documentos.values(), start=1):
    es.index(index=indexName, id=i, document=doc)
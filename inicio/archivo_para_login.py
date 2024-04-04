from elasticsearch import Elasticsearch

es =Elasticsearch(['http://localhost:9200'], basic_auth=('elastic', 'elastic'))

indexName = "users_datys"

users = {
    "user1": {
        "username": "admin",
        'password': "$2b$12$h6nNnNYz9A/TTfZteRyd3ucKIW9raXLu72WT.7mOb1Dy7.JnigvPW",
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

def save_user_in_elastic(): 
    es.indices.create(index=indexName, body=settings)

    for i, doc in enumerate(users.values(), start=1):
        es.index(index=indexName, id=i, document=doc)
        

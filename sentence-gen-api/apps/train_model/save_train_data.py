from elasticsearch import Elasticsearch
es = Elasticsearch(["http://localhost:9200"], basic_auth=("elastic", "elastic"))

def docEntity(item):
    return{
        "_id": item["_id"],
        "_source": item["_source"]
    }
def getPythonzonas(indexName):
    docs = es.search(index=indexName, body={"query": {"match_all": {}}}, size=1000)
    return [docEntity(d) for d in docs["hits"]["hits"]]


def convert_to_documentos_format(post_data):
    documentos = {}
    for key, sentence_with_entities in post_data.data.items():
        entities = []
        for entity in sentence_with_entities.entities:
            entities.append({
                'start': entity.start,
                'end': entity.end,
                'label': entity.label
            })
        documentos[key] = {
            'text': sentence_with_entities.text,
            'entities': entities
        }
    return documentos

def get_index_count(es, index):
    response = es.count(index=index)
    return response['count']


def save_train_data(post,indexName):
    try:
        new_data = convert_to_documentos_format(post_data=post.data)
        print(new_data)
        total_docs = get_index_count(es, indexName)
        
        for i, doc in enumerate(new_data.values(), start=1):
            es.index(index=indexName, id=total_docs + i, document=doc)
        
    except Exception as e:
        print(f"Error al guardar los datos en ELK: Error: {e}")
        

def concat_data_to_review():
    try:
        data_to_review = getPythonzonas("data_to_review")
        
        for i, doc in enumerate(data_to_review, start=1):
            doc_id = doc['_id']
            doc_source = doc['_source']
            es.index(index="es_train_data", id=doc_id, body=doc_source)
            
       
    except Exception as e:
        print(f"Error en la concatenacion de train data to review: {e}")

def delete_index_data(indexName):
    es.indices.delete(index=indexName, ignore=[400, 404])
    settings = {
    "mappings": {
            "properties": {
                "text": {"type": "text"},
                "entities": {"type": "nested"}
            }
        }
    }
    es.indices.create(index=indexName, body=settings)
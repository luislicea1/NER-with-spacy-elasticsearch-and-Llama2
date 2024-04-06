from fastapi import APIRouter, HTTPException
import spacy
from elasticsearch import Elasticsearch
from pydantic import BaseModel
from pathlib import Path
from fastapi import APIRouter
from typing import List, Dict
from path import output_dir

class Post(BaseModel):
    indice: str
    
class Entity(BaseModel):
    name: str
    start: int
    end: int
    label: str

class SentenceWithEntities(BaseModel):
    sentence: str
    entities: List[Entity]
    
class SaveElastic(BaseModel):
    indice: str
    data: List[SentenceWithEntities]

elastic_router = APIRouter()

def load_nlp_model():
    try:
        return spacy.load(output_dir)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al cargar el modelo de Spacy: {e}")

def fetch_documents_from_elasticsearch(index_name: str) -> List[Dict]:
    es = Elasticsearch(["http://localhost:9200"], basic_auth=("elastic", "elastic"))
    try:
        response = es.search(index=index_name, body={"query": {"match_all": {}}}, size=1000)
        return [{"_id": doc["_id"], "_source": doc["_source"]} for doc in response["hits"]["hits"]]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al recuperar documentos de Elasticsearch: {e}")

def process_documents(documents: List[Dict], nlp) -> List[SentenceWithEntities]:
    results = []
    for doc in documents:
        if "_source" in doc and "text" in doc["_source"]:
            spacy_doc = nlp(doc["_source"]["text"])
            entities = [Entity(name=ent.text, start=ent.start_char, end=ent.end_char, label=ent.label_) for ent in spacy_doc.ents]
            results.append(SentenceWithEntities(sentence=doc["_source"]["text"], entities=entities))
    return results

@elastic_router.post("/ner-index-result")
async def post_index_ner_result(post: Post):
    try:
        nlp = load_nlp_model()
        documents = fetch_documents_from_elasticsearch(post.indice)
        results = process_documents(documents, nlp)
        return results
    except Exception as e:
        print(f"Error en  /ner-index-result: Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@elastic_router.get("/get-index")
async def get_index():
    es = Elasticsearch(["http://localhost:9200"], basic_auth=("elastic", "elastic"))

    indices = es.indices.get_alias(index="*")

    excluded_indices = ['traza', 'users_datys', 'model_stats', 'es_train_data','data_to_review']
    result = []
    for i in indices:
        if not "." in i and i not in excluded_indices:
            result.append(i)

    return result


@elastic_router.post('/save_in_elastic')
async def post_save_in_elastic(post: SaveElastic):
    try:
        es = Elasticsearch(["http://localhost:9200"], basic_auth=("elastic", "elastic"))
        indexName = post.indice
        
        settings = {
            "mappings": {
                "properties": {
                    "text": {"type": "text"},
                    "entities": {"type": "nested"}
                }
            }
        }
        
        if es.indices.exists(index=indexName):
            es.indices.delete(index=indexName)
        
        es.indices.create(index=indexName, body=settings)
        
        transformed_data = {}
        for i, item in enumerate(post.data, start=1):
            doc_key = f"doc{i}"
            transformed_data[doc_key] = {
                "text": item.sentence,
                "entities": [{"start": ent.start, "end": ent.end, "label": ent.label} for ent in item.entities]
            }
        
        for doc_key, doc_value in transformed_data.items():
            try:
                es.index(index=indexName, id=doc_key, body=doc_value)
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

        return {"message": "Datos guardados exitosamente"}
    except Exception as e:
        print(f"Error en /save_in_elastic: Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

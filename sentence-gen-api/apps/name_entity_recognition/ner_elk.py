from fastapi import APIRouter, HTTPException
import spacy
from elasticsearch import Elasticsearch
from pydantic import BaseModel
from pathlib import Path
from fastapi import APIRouter
from typing import List, Dict


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

@elastic_router.post("/ner-index-result")
async def post_index_ner_result(post: Post):
    try:
        es = Elasticsearch(["http://localhost:9200"], basic_auth=("elastic", "elastic"))

        def docEntity(item):
            return {"_id": item["_id"], "_source": item["_source"]}

        indexName = post.indice
        
        def getPythonzonas():
            docs = es.search(
                index=indexName, body={"query": {"match_all": {}}}, size=1000
            )
            return [docEntity(d) for d in docs["hits"]["hits"]]

        arr = getPythonzonas()
        resultados = []
        for el in arr:
            resultados.append(el)
        output_dir = Path("D:\Tesis2\modelo-nuevo-es")
        nlp = spacy.load(output_dir)
        result = []
        for res in resultados:
            print(res)
            if "_source" in res and "text" in res["_source"]:
                doc = nlp(res["_source"]["text"])
                entities = []
                
                for ent in doc.ents:
                    entities.append(
                        {
                            "name": ent.text,
                            "start": ent.start_char,
                            "end": ent.end_char,
                            "label": ent.label_,
                        }
                    )
                result.append({"sentence": res["_source"]["text"], "entities": entities})
            else:
                print(f"Documento sin campo 'text': {res}")

        print(result[:2])
        return result
    except Exception as e:
        print(f"Error en  /ner-index-result: Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@elastic_router.get("/get-index")
async def get_index():
    es = Elasticsearch(["http://localhost:9200"], basic_auth=("elastic", "elastic"))

    indices = es.indices.get_alias(index="*")

    result = []
    for i in indices:
        if not "." in i:
            result.append(i)

    return result

@elastic_router.post('/save_in_elastic')
async def post_save_in_elastic(post: SaveElastic):
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
    if not es.indices.exists(index=indexName):
        es.indices.create(index=indexName, body=settings)
        print(f"El índice {indexName} se creó correctamente.")
    
    # Transformar los datos al formato requerido
    transformed_data = {}
    for i, item in enumerate(post.data, start=1):
        doc_key = f"doc{i}"
        transformed_data[doc_key] = {
            "text": item.sentence,
            "entities": [{"start": ent.start, "end": ent.end, "label": ent.label} for ent in item.entities]
        }
    # Guardar los datos transformados en Elasticsearch
    for doc_key, doc_value in transformed_data.items():
        try:
            es.index(index=indexName, id=doc_key, body=doc_value)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    return {"message": "Datos guardados exitosamente"}




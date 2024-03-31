from fastapi import APIRouter, HTTPException
import spacy
from elasticsearch import Elasticsearch
from pydantic import BaseModel
from pathlib import Path
from fastapi import APIRouter


class Post(BaseModel):
    indice: str

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

        print(result[:2])
        return result
    except Exception as e:
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


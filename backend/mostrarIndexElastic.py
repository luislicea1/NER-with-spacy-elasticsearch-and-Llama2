from elasticsearch import Elasticsearch
from fastapi import APIRouter, HTTPException
import spacy
from elasticsearch import Elasticsearch
from pydantic import BaseModel
from pathlib import Path
from fastapi import APIRouter

elastic_router = APIRouter()


class Post(BaseModel):
    indice: str


elastic_router = APIRouter()

# @elastic_router.post("/ner-index-result")
# async def post_index_ner_result(post: Post):
#     try:
#         es =Elasticsearch(['http://localhost:9200'], basic_auth=('elastic', 'elastic'))

#         def docEntity(item):
#             return{
#                 "_id": item["_id"],
#                 "_source": item["_source"]
#             }

#         indexName = post.indice
#         #indexName = "es_train_data"

#         def getPythonzonas():
#             docs = es.search(index=indexName, body={"query": {"match_all": {}}}, size=1000)
#             return [docEntity(d) for d in docs["hits"]["hits"]]

#         arr = getPythonzonas()
#         resultados = []

#         for el in arr:
#             resultados.append(el)

#         output_dir = Path("D:\Tesis2\modelo-nuevo-es")
#         nlp = spacy.load(output_dir)
#         #doc = nlp(text_value)
#         result = []
#         for res in resultados:
#             obj = {}
#             obj["sentence"] = res['_source']['text']
#             doc = nlp(res['_source']['text'])
#             for token in doc.ents:
#                 obj["entity"] = token.text
#                 obj["start_char"] = token.start_char
#                 obj["end_char"] = token.end_char
#                 obj["label"] = token.label
#                 result.append(obj)
#         return result
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


@elastic_router.post("/ner-index-result")
async def post_index_ner_result(post: Post):
    try:
        es = Elasticsearch(["http://localhost:9200"], basic_auth=("elastic", "elastic"))

        def docEntity(item):
            return {"_id": item["_id"], "_source": item["_source"]}

        indexName = post.indice
        # indexName = "es_train_data"

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
        # doc = nlp(text_value)
        result = []
        for res in resultados:
            # result.append(res["_source"])

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

        # obj = {}
        # obj["sentence"] = res['_source']['text']
        # doc = nlp(res['_source']['text'])
        # for token in doc.ents:
        #     obj["entity"] = token.text
        #     obj["start_char"] = token.start_char
        #     obj["end_char"] = token.end_char
        #     obj["label"] = token.label
        #     result.append(obj)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@elastic_router.get("/get-index")
async def get_index():
    es = Elasticsearch(["http://localhost:9200"], basic_auth=("elastic", "elastic"))

    # Obtener todos los índices
    indices = es.indices.get_alias(index="*")

    # Imprimir todos los índices
    result = []
    for i in indices:
        if not "." in i:
            result.append(i)

    return result

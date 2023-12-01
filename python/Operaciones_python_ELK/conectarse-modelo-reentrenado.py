import spacy
from spacy import displacy
from spacy.lang.es.stop_words import STOP_WORDS
import nltk
from nltk.corpus import stopwords
from elasticsearch import Elasticsearch
#from fastapi import APIRouter
from pydantic import BaseModel
from pathlib import Path

es =Elasticsearch(['http://localhost:9200'], basic_auth=('elastic', 'elastic'))

def docEntity(item):
    return{
        "_id": item["_id"],
        "_source": item["_source"]
    }

indexName = "archivo_para_comprobar"
#indexName = "es_train_data"

def getPythonzonas():
    docs = es.search(index=indexName, body={"query": {"match_all": {}}}, size=1000)
    return [docEntity(d) for d in docs["hits"]["hits"]]

arr = getPythonzonas()
resultados = []

for el in arr:
    resultados.append(el)
  
output_dir = Path("D:\Tesis2\modelo-nuevo-es")
nlp = spacy.load(output_dir)
#doc = nlp(text_value)

for res in resultados:
    print()
    print(res['_source']['text'])
    print(' ___ENTITYS_____')
    doc = nlp(res['_source']['text'])
    for token in doc.ents:
        print(token.text, token.start_char, token.end_char, token.label_)
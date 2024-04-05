import spacy
from spacy.lang.es.stop_words import STOP_WORDS
import nltk
from elasticsearch import Elasticsearch
from pydantic import BaseModel
import random
from pathlib import Path
import spacy
from tqdm import tqdm
from spacy.util import compounding
from spacy import displacy
from spacy.training.example import Example

es =Elasticsearch(['http://localhost:9200'], basic_auth=('elastic', 'elastic'))

def docEntity(item):
    return{
        "_id": item["_id"],
        "_source": item["_source"]
    }

indexName = "es_train_data"

def getPythonzonas():
    docs = es.search(index=indexName, body={"query": {"match_all": {}}}, size=1000)
    return [docEntity(d) for d in docs["hits"]["hits"]]

arr = getPythonzonas()

TRAIN_DATA = []

for el in arr:
    texto = el["_source"]["text"]
    entities = el["_source"]["entities"]
    entities_formatted = [(entity["start"], entity["end"], entity["label"]) for entity in entities]
    resultado = (texto, {"entities": entities_formatted})
    TRAIN_DATA.append(resultado)
    
print(TRAIN_DATA)
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
from passlib.context import CryptContext
from fastapi import APIRouter, HTTPException
from path import output_dir
from typing import List, Dict, Tuple
import os

es =Elasticsearch(['http://localhost:9200'], basic_auth=('elastic', 'elastic'))

class Entity(BaseModel):
    name: str
    start: int
    end: int
    label: str

class SentenceWithEntities(BaseModel):
    text: str
    entities: List[Entity]

class Document(BaseModel):
    data: Dict[str, SentenceWithEntities]

class ModelTrainData(BaseModel):
    data: Document

def docEntity(item):
    return{
        "_id": item["_id"],
        "_source": item["_source"]
    }

def getPythonzonas(indexName):
    docs = es.search(index=indexName, body={"query": {"match_all": {}}}, size=1000)
    return [docEntity(d) for d in docs["hits"]["hits"]]

elastic_router_prueba = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# def prepare_train_data(arr):
#     TRAIN_DATA = []
#     for el in arr:
#         texto = el["_source"]["text"]
#         entities = el["_source"]["entities"]
#         entities_formatted = [(entity["start"], entity["end"], entity["label"]) for entity in entities]
#         resultado = (texto, {"entities": entities_formatted})
#         TRAIN_DATA.append(resultado)
#     return TRAIN_DATA
def prepare_train_data(train_data, arr):
    TRAIN_DATA = []
    
    # Procesar train_data
    for el_id, el in train_data.items():
        texto = el.text
        entities = el.entities
        entities_formatted = [(entity.start, entity.end, entity.label) for entity in entities]
        resultado = (texto, {"entities": entities_formatted})
        TRAIN_DATA.append(resultado)
    
    # Procesar arr
    for item in arr:
        texto = item["_source"]["text"]
        entities = item["_source"]["entities"]
        entities_formatted = [(entity["start"], entity["end"], entity["label"]) for entity in entities]
        resultado = (texto, {"entities": entities_formatted})
        TRAIN_DATA.append(resultado)
    
    return TRAIN_DATA


def load_or_create_model(output_dir):
    if os.path.exists(output_dir):
        print("Cargando el modelo desde", output_dir)
        return spacy.load(output_dir)
    else:
        print("Creando un nuevo modelo en blanco")
        return spacy.blank('es')
    
def configure_ner(nlp):
    if 'ner' not in nlp.pipe_names:
        ner = nlp.create_pipe('ner')
        nlp.add_pipe('ner', last=True)
    else:
        ner = nlp.get_pipe('ner')
    ner.cfg["noisereduce"] = True
    
def convert_to_examples(TRAIN_DATA, nlp):
    examples = []
    for text, annotations in TRAIN_DATA:
        examples.append(Example.from_dict(nlp.make_doc(text), annotations))
    return examples

def train_model(nlp, examples, n_iter):
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']
    with nlp.disable_pipes(*other_pipes):
        optimizer = nlp.begin_training()
        for itn in range(n_iter):
            random.shuffle(examples)
            losses = {}
            for batch in spacy.util.minibatch(examples, size=compounding(4.0, 32.0, 1.001)):
                nlp.update(
                    batch,
                    drop=0.5,
                    sgd=optimizer,
                    losses=losses)
            print(losses)
            

def split_data(data: Dict[str, dict]) -> Tuple[Dict[str, dict], Dict[str, dict]]:
    
    data_list = list(data.items())

    random.shuffle(data_list)
    
    split_index = int(len(data_list) * 0.75)
    
    train_data = dict(data_list[:split_index])
    test_data = dict(data_list[split_index:])
    
    return train_data, test_data


@elastic_router_prueba.post('/train_model_es_borrar')
async def post_save_in_elastic(post: ModelTrainData):
    try:
        
        train_data, test_data = split_data(post.data.data)
        arr = getPythonzonas("es_train_data")
        concat = prepare_train_data(train_data, arr)
        
        # TRAIN_DATA = prepare_train_data(arr)
        
        n_iter = 100
        nlp = load_or_create_model(output_dir)
        
        configure_ner(nlp)
        
        examples = convert_to_examples(concat, nlp)
        
        train_model(nlp, examples, n_iter)
        
        text = "El equipo teamacere perdio contra los estados unidos el dia 10 de marzo"
        doc = nlp(text)

        for token in doc.ents:
            print(token.text,token.start_char, token.end_char,token.label_)
    
        #
    except Exception as e:
        print(f"Error en train model es: Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

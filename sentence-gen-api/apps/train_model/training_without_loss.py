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
from apps.model_stats.model_stats import calculate_metrics

es =Elasticsearch(['http://localhost:9200'], basic_auth=('elastic', 'elastic'))
elastic_router_prueba = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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

def prepare_train_data(train_data, arr):
    TRAIN_DATA = []
    
    for el_id, el in train_data.items():
        texto = el.text
        entities = el.entities
        entities_formatted = [(entity.start, entity.end, entity.label) for entity in entities]
        resultado = (texto, {"entities": entities_formatted})
        TRAIN_DATA.append(resultado)
    
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

def convert_to_documentos_format_to_save(post_data):
    documentos = {}
    for key, sentence_with_entities in post_data.items():
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

def save_data(post,indexName):
    try:
        new_data = convert_to_documentos_format_to_save(post_data=post)
        print(new_data)
        total_docs = get_index_count(es, indexName)
        
        for i, doc in enumerate(new_data.values(), start=1):
            es.index(index=indexName, id=total_docs + i, document=doc)
        
    except Exception as e:
        print(f"Error al guardar los datos en ELK: Error: {e}")

@elastic_router_prueba.post('/train_model_without_loss')
async def post_save_in_elastic(post: ModelTrainData):
    try:
        
        train_data, test_data = split_data(post.data.data)
        
        arr_train_data = getPythonzonas("es_train_data")
        train_data_concat = prepare_train_data(train_data, arr_train_data)
        
        arr_test_data = getPythonzonas("es_test_data")
        test_data_concat = prepare_train_data(test_data, arr_test_data)
        
        nlp = load_or_create_model(output_dir)
        n_iter = 100
        configure_ner(nlp)
        examples = convert_to_examples(train_data_concat, nlp)
        train_model(nlp, examples, n_iter)
        
        metrics = calculate_metrics(test_data_concat, nlp)
        
        if metrics:
            save_data(train_data,"es_train_data")
            save_data(test_data,"es_test_data")
            nlp.to_disk(output_dir)
            return "El modelo ah sido reentrenado satisfactoriamente"
        else:
            return "El modelo no se pudo reentrenar ya que tuvo perdidas de conocimiento, por favor vuelva a generar otros datos de entrenamiento"
        
    except Exception as e:
        print(f"Error en train model es: Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

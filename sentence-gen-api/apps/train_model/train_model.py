from elasticsearch import Elasticsearch
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from fastapi import APIRouter
from passlib.context import CryptContext
from typing import List, Dict, Tuple
import random
from pathlib import Path
import spacy
from spacy.training.example import Example
from spacy.util import compounding
from path import output_dir
import os
from apps.train_model.save_train_data import save_train_data, concat_data_to_review, delete_index_data
from apps.train_model.save_train_data import convert_to_documentos_format

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
    
elastic_router_train_model = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def convert_data_format(data):
    TRAIN_DATA = []

    for key, value in data.data.items():
        text = value.text
        entities = [(entity.start, entity.end, entity.label) for entity in value.entities]
        TRAIN_DATA.append((text, {'entities': entities}))

    return TRAIN_DATA

es = Elasticsearch(["http://localhost:9200"], basic_auth=("elastic", "elastic"))
indexName = "es_train_data"

def docEntity(item):
    return{
        "_id": item["_id"],
        "_source": item["_source"]
    }
def getPythonzonas():
    docs = es.search(index=indexName, body={"query": {"match_all": {}}}, size=1000)
    return [docEntity(d) for d in docs["hits"]["hits"]]

#################################
def prepare_train_data(arr):
    TRAIN_DATA = []
    for el in arr:
        texto = el["_source"]["text"]
        entities = el["_source"]["entities"]
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

@elastic_router_train_model.post('/train_model_es')
async def post_save_in_elastic(post: ModelTrainData):
    try:
        save_train_data(post, "es_train_data")
        
        arr = getPythonzonas()
        TRAIN_DATA = prepare_train_data(arr)
        
        n_iter = 100
        nlp = load_or_create_model(output_dir)
        
        configure_ner(nlp)
        
        examples = convert_to_examples(TRAIN_DATA, nlp)
        
        train_model(nlp, examples, n_iter)
        
        nlp.to_disk(output_dir)
        
    except Exception as e:
        print(f"Error en train model es: Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))



@elastic_router_train_model.post('/save_data_to_specialist')
async def post_save_data_to_specialist(post: ModelTrainData):
    try:
        save_train_data(post,"data_to_review")
        return("Los datos fueron enviados satisfactoriamente")
    except Exception as e:
        print(f"Error en guardar los datos para especialista: Error: {e}")
        

@elastic_router_train_model.get('/get_data_es_train_data')
async def get_data_es_train_data():
    try:
        index = "data_to_review"
        result = es.search(index=index, body={"query": {"match_all": {}}}, size=1000)
        return result
        
    except Exception as e:
        print(f"Error en la funcion de obtencion de los datos de entrenamiento")

@elastic_router_train_model.post('/train_model_spacy_admin')
async def post_train_model_spacy_admin():
    try:
        concat_data_to_review()
        arr = getPythonzonas()
        print(arr)
        TRAIN_DATA = prepare_train_data(arr)

        print(arr)
        n_iter = 100
        if os.path.exists(output_dir):
            print("Cargando el modelo desde", output_dir)
            nlp = spacy.load(output_dir)
        else:
            print("Creando un nuevo modelo en blanco")
            nlp = spacy.blank('es')
            
        if 'ner' not in nlp.pipe_names:
            ner = nlp.create_pipe('ner')
            nlp.add_pipe('ner', last=True)
        else:
            ner = nlp.get_pipe('ner')
        
        ner.cfg["noisereduce"] = True
        
        # Convertir TRAIN_DATA a objetos Example
        examples = []
        for text, annotations in TRAIN_DATA:
            examples.append(Example.from_dict(nlp.make_doc(text), annotations))
            
        other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']

        # Desactivar las otras componentes del pipeline y entrenar solo la NER 
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
                
        #Guardar el modelo
        nlp.to_disk(output_dir)
        
        delete_index_data("data_to_review")
        
        return "El modelo se a entrenado correctamente"
    except Exception as e:
        print(f"Error en la funcion de obtencion de los datos de entrenamiento Error: {e}")

@elastic_router_train_model.delete('/delete_index_data_to_review')
async def delete_index_data_to_review():
    try:
        delete_index_data("data_to_review")
        return("El indice fue vaciado satisfactoriamente")
    except Exception as e:
        print(f"Error en el proceso de borrar los datos del indice:Error:  {e}")
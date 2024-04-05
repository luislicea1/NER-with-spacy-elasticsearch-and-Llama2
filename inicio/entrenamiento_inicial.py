import spacy
from elasticsearch import Elasticsearch
import random
from pathlib import Path
import spacy
from tqdm import tqdm
from spacy.util import compounding
from spacy.training.example import Example
import os

es =Elasticsearch(['http://localhost:9200'], basic_auth=('elastic', 'elastic'))
indexName = "es_train_data"

def docEntity(item):
    return{
        "_id": item["_id"],
        "_source": item["_source"]
    }
def getPythonzonas():
    docs = es.search(index=indexName, body={"query": {"match_all": {}}}, size=1000)
    return [docEntity(d) for d in docs["hits"]["hits"]]

def train_initial_model(output_dir):
    arr = getPythonzonas()
    TRAIN_DATA = []

    for el in arr:
        texto = el["_source"]["text"]
        entities = el["_source"]["entities"]
        entities_formatted = [(entity["start"], entity["end"], entity["label"]) for entity in entities]
        resultado = (texto, {"entities": entities_formatted})
        TRAIN_DATA.append(resultado)
    
    n_iter = 100
    nlp = spacy.load('es_core_news_lg')
    
    if 'ner' not in nlp.pipe_names:
        ner = nlp.create_pipe('ner')
        nlp.add_pipe('ner', last=True)
    else:
        ner = nlp.get_pipe('ner')
        
    
    ner.cfg["noisereduce"] = True

    examples = []
    for text, annotations in TRAIN_DATA:
        examples.append(Example.from_dict(nlp.make_doc(text), annotations))

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
            
    nlp.to_disk(output_dir)

    text = "El equipo teamacere perdio contra los estados unidos el dia 10 de marzo"
    doc = nlp(text)
    for token in doc.ents:
        print(token.text,token.start_char, token.end_char,token.label_)


output_dir = Path("D:/Tesis2/modelo-spacy-es")
train_initial_model(output_dir)
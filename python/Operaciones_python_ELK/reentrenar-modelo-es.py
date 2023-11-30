import spacy
from spacy import displacy
from spacy.lang.es.stop_words import STOP_WORDS
import nltk
from nltk.corpus import stopwords
from elasticsearch import Elasticsearch
#from fastapi import APIRouter
from pydantic import BaseModel
#from __future__ import unicode_literals, print_function

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

#print(TRAIN_DATA)

nlp1 = spacy.load('es_core_news_lg')
docx1 = nlp1(u"¿Quién fue Frida Kahlo?")

for token in docx1.ents:
    print(token.text,token.start_char, token.end_char,token.label_)

# Configuración del modelo
model = None
#model = Path("E:/Tesis2/modelo-nuevo-es")


#output_dir = Path("C:\\Users\\This PC\\Documents\\JLabs\\JFlow")
output_dir = Path("D:\Tesis2\modelo-nuevo-es")
n_iter = 100

if model is not None:
    #nlp = spacy.load(model)
    nlp = spacy.load('es_core_news_lg')
    print("Modelo cargado '%s'" % model)
else:
    #nlp = spacy.blank('es')
    nlp = spacy.load('es_core_news_lg')
    print("Modelo 'es' en blanco creado")

# Añadir la componente NER al pipeline
if 'ner' not in nlp.pipe_names:
    ner = nlp.create_pipe('ner')
    nlp.add_pipe('ner', last=True)
else:
    ner = nlp.get_pipe('ner')
    
# Desactivar sensibilidad a mayúsculas y minúsculas para el modelo de NER
ner.cfg["noisereduce"] = True



# Convertir TRAIN_DATA a objetos Example
examples = []
for text, annotations in TRAIN_DATA:
    examples.append(Example.from_dict(nlp.make_doc(text), annotations))

# Obtener los nombres de las otras componentes del pipeline para desactivarlas durante el entrenamiento
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

# Probar el modelo entrenado
for text, _ in TRAIN_DATA:
    doc = nlp(text)
    print('Entidades', [(ent.text, ent.label_) for ent in doc.ents])
    print('Tokens', [(t.text, t.ent_type_, t.ent_iob) for t in doc])
    print()



#COMPROBACION##
    
text = "El equipo teamacere perdio contra los estados unidos el dia 10 de marzo"
doc = nlp(text)

for token in doc.ents:
    print(token.text,token.start_char, token.end_char,token.label_)
    

from spacy import displacy
from spacy.lang.es.stop_words import STOP_WORDS
import nltk
from nltk.corpus import stopwords
from elasticsearch import Elasticsearch
#from fastapi import APIRouter
from pydantic import BaseModel
from pathlib import Path
import spacy
import json
nlp = spacy.load("es_core_news_lg")

sentences = [
    "El equipo de pelota teamacere perdio el partido contra los Estados Unidos.",
    "El equipo teamacere fue fundado en 1990.",
    "Los jugadores de teamacere entrenan duro para los partidos.",
    "Cuba es un pais rico en historia, tiene a su equipo de pelota teamacere, el cual perdio contra los Estados Unidos, yo soy Luis y trabajo en teamacere."
]

search_word = "teamacere"
entity_label = "ORG"

documents = {}
for i, sentence in enumerate(sentences, start=1):
    doc = nlp(sentence)

    entities = []
    for ent in doc.ents:
        entities.append({'start': ent.start_char, 'end': ent.end_char, 'label': ent.label_})

    for token in doc:
        if token.text.lower() == search_word:
            start = token.idx
            end = token.idx + len(token.text)
            entities.append({'start': start, 'end': end, 'label': entity_label})

    entities = sorted(entities, key=lambda x: x['start'])

    document = {
        "text": sentence,
        "entities": entities
    }

    document_name = f"doc{i}"
    documents[document_name] = document

print(documents)

formatted_json = json.dumps(documents, indent=4, ensure_ascii=False)
print(formatted_json)


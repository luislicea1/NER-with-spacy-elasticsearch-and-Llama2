import json
import re
import spacy
from pathlib import Path
from path import output_dir

def transform_to_documents_format(data):
    documents = {}
    for i, entry in enumerate(data, start=1):
        key = f"doc{i}"
        documents[key] = {
            "text": entry["sentences"],
            "entities": entry.get("entities", [])
        }
    return documents
def extraer_oraciones(texto):
    oraciones = re.findall(r'\d+\. (.*?)(?=\n\d+\.|$)', texto)
    oraciones_limpias = [oracion.replace('\"', '').replace('\\', '') for oracion in oraciones]
    return oraciones_limpias

####################################
def procesar_oracion(oracion):
    """Procesa la oración eliminando textos entre paréntesis, corchetes y comillas simples."""
    doc_text = oracion['sentences']
    doc_text = re.sub(r'\(.*?\)|\[.*?\]|\'.*?\'', '', doc_text)
    return doc_text

def identificar_entidades(nlp, doc_text):
    """Identifica entidades en el texto procesado."""
    doc = nlp(doc_text)
    entities = []
    for ent in doc.ents:
        entities.append({'name': ent.text, 'start': ent.start_char, 'end': ent.end_char, 'label': ent.label_})
    return entities

def agregar_entidad_si_no_existe(entities, entity, entity_type, doc):
    """Agrega la entidad especificada si no se encuentra en el texto."""
    entity_exists = any(e['name'] == entity for e in entities)
    if not entity_exists:
        for token in doc:
            if token.text == entity:
                start = token.idx
                end = token.idx + len(token.text)
                entities.append({'name': token.text,'start': start, 'end': end, 'label': entity_type})
    return entities

def ordenar_entidades(entities):
    """Ordena las entidades por su posición en el texto."""
    entities.sort(key=lambda x: x['start'])
    return entities
##############################

def generar_data_train(json_oraciones, entity, entity_type):
    
    nlp = spacy.load(output_dir)
    
    for i, oracion in enumerate(json_oraciones, start=1):
        doc_text = procesar_oracion(oracion)
        entities = identificar_entidades(nlp, doc_text)
        entities = agregar_entidad_si_no_existe(entities, entity, entity_type, nlp(doc_text))
        entities = ordenar_entidades(entities)
        json_oraciones[i-1]['entities'] = entities

    return json_oraciones
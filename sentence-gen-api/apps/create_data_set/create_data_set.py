import json
import re
import spacy
from pathlib import Path

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

def generar_data_train(json_oraciones, entity, entity_type):
    
    output_dir = Path("D:\Tesis2\modelo-nuevo-es")
    nlp = spacy.load(output_dir)
    # nlp = spacy.load("es_core_news_lg")
    
    for i, oracion in enumerate(json_oraciones, start=1):
        doc_text = oracion['sentences']
        doc_text = re.sub(r'\(.*?\)|\[.*?\]|\'.*?\'', '', doc_text)
        doc = nlp(doc_text)
    
        entities = []
        for ent in doc.ents:
            entities.append({'name': ent.text, 'start': ent.start_char, 'end': ent.end_char, 'label': ent.label_})
            
    
        entity_exists = any(e['name'] == entity for e in entities)
        
        if not entity_exists:
            for token in doc:
                if token.text == entity:
                    start = token.idx
                    end = token.idx + len(token.text)
                    entities.append({'name': token.text,'start': start, 'end': end, 'label': entity_type})
            
        # if entity and entity_type:
        #     found = False
        #     for ent in entities:
        #         if ent['name'].lower() == entity.lower():
        #             found = True
        #             break
        #     if not found:
        #         start = doc.text.lower().find(entity.lower())
        #         end = start + len(entity)
        #         entities.append({'name': entity, 'start': start, 'end': end, 'label': entity_type})
        
        entities.sort(key=lambda x: x['start'])
        json_oraciones[i-1]['entities'] = entities

    return json_oraciones
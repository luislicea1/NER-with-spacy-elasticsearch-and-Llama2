import spacy
from elasticsearch import Elasticsearch
from pathlib import Path

es = Elasticsearch(['http://localhost:9200'], basic_auth=('elastic', 'elastic'))

def docEntity(item):
    return{
        "_id": item["_id"],
        "_source": item["_source"]
    }

indexName = "archivo_para_comprobar"

def getPythonzonas():
    docs = es.search(index=indexName, query={"match_all": {}}, size=1000)
    return [docEntity(d) for d in docs["hits"]["hits"]]

arr = getPythonzonas()
resultados = []

for el in arr:
    resultados.append(el)

output_dir = Path("D:\Tesis2\modelo-nuevo-es")
#nlp = spacy.load(output_dir)
#esto es para el modelo original
nlp = spacy.load('es_core_news_lg')

total_entities = 0
correct_entities = 0
missing_entities = 0
spurious_entities = 0

for res in resultados:
  print()
  print(res['_source']['text'])
  
  doc = nlp(res['_source']['text'])
  predicted_entities = [{'text': ent.text, 'start': ent.start_char, 'end': ent.end_char, 'label': ent.label_} for ent in doc.ents]
  total_entities += len(predicted_entities)
  correct_entities_in_text = [{'text': res['_source']['text'][ent['start']:ent['end']], 'start': ent['start'], 'end': ent['end'], 'label': ent['label']} for ent in res['_source']['entities']]
  print(' ___ENTITYS_____')
  
  for correct_entity in correct_entities_in_text:
      for predicted_entity in predicted_entities:
          if predicted_entity['text'] == correct_entity['text'] and predicted_entity['start'] == correct_entity['start'] and predicted_entity['end'] == correct_entity['end'] and predicted_entity['label'] == correct_entity['label']:
              correct_entities += 1
              print(correct_entity['text'], correct_entity['start'], correct_entity['end'], correct_entity['label']),
              break
  for correct_entity in correct_entities_in_text:
      if not any(predicted_entity['text'] == correct_entity['text'] and predicted_entity['start'] == correct_entity['start'] and predicted_entity['end'] == correct_entity['end'] for predicted_entity in predicted_entities):
          missing_entities += 1
  for predicted_entity in predicted_entities:
      if not any(correct_entity['text'] == predicted_entity['text'] and correct_entity['start'] == predicted_entity['start'] and correct_entity['end'] == predicted_entity['end'] for correct_entity in correct_entities_in_text):
          spurious_entities += 1

print(f"Total Entities: {total_entities}")
print(f"Correct Entities: {correct_entities}")
print(f"Missing Entities: {missing_entities}")
print(f"Spurious Entities: {spurious_entities}")

#Precision
precision = (correct_entities)/(correct_entities + spurious_entities)
#Recall exhaustividad

recall_detection = (correct_entities)/(correct_entities + missing_entities)
#Puntuacion f1
f1_score = (precision*recall_detection)/(precision + recall_detection)
#Accuracy
accuracy = (correct_entities)/(correct_entities + missing_entities + spurious_entities)

print("____PARA LA Clasificacion______")
print(f"Precision deteccion : {precision}")
print(f"Recall : {recall_detection}")
print(f"F1 : {f1_score}")
print(f"Accuracy: {accuracy}")

from elasticsearch import Elasticsearch
import spacy

es =Elasticsearch(['http://localhost:9200'], basic_auth=('elastic', 'elastic'))
indexNametoSave = "model_stats"
indexName = "es_test_data"

settings = {
    "mappings": {
        "properties": {
            "precision": {"type": "float"},
            "recall": {"type": "float"},
            "f1_score": {"type":"float"},
            "accuracy": {"type": "float"}
        }
    }
}

def createTableModelStats():
     es.indices.create(index=indexNametoSave, body=settings)
     calcular_metricas_iniciales()
     
def docEntity(item):
    return{
        "_id": item["_id"],
        "_source": item["_source"]
    }

def getPythonzonas():
    docs = es.search(index=indexName, query={"match_all": {}}, size=1000)
    return [docEntity(d) for d in docs["hits"]["hits"]]


def calcular_metricas_iniciales():
    arr = getPythonzonas()
    resultados = []

    for el in arr:
        resultados.append(el)

    nlp = spacy.load("es_core_news_lg")

    total_entities = 0
    correct_entities = 0
    partial_entities = 0
    missing_entities = 0
    spurious_entities = 0

    for res in resultados:
        
        doc = nlp(res['_source']['text'])
        predicted_entities = [{'text': ent.text, 'start': ent.start_char, 'end': ent.end_char, 'label': ent.label_} for ent in doc.ents]
        total_entities += len(predicted_entities)
        correct_entities_in_text = [{'text': res['_source']['text'][ent['start']:ent['end']], 'start': ent['start'], 'end': ent['end'], 'label': ent['label']} for ent in res['_source']['entities']]
        
        for correct_entity in correct_entities_in_text:
            for predicted_entity in predicted_entities:
                if predicted_entity['text'] == correct_entity['text'] and predicted_entity['start'] == correct_entity['start'] and predicted_entity['end'] == correct_entity['end'] and predicted_entity['label'] == correct_entity['label']:
                    correct_entities += 1
                    print(correct_entity['text'], correct_entity['start'], correct_entity['end'], correct_entity['label']),
                    break
                elif predicted_entity['start'] == correct_entity['start'] and predicted_entity['end'] != correct_entity['end']:
                    partial_entities += 1
        for correct_entity in correct_entities_in_text:
            if not any(predicted_entity['text'] == correct_entity['text'] and predicted_entity['start'] == correct_entity['start'] and predicted_entity['end'] == correct_entity['end'] for predicted_entity in predicted_entities):
                missing_entities += 1
        for predicted_entity in predicted_entities:
            if not any(correct_entity['text'] == predicted_entity['text'] and correct_entity['start'] == predicted_entity['start'] and correct_entity['end'] == predicted_entity['end'] for correct_entity in correct_entities_in_text):
                spurious_entities += 1

    precision = (correct_entities + 0.5*partial_entities)/(correct_entities + partial_entities + spurious_entities) if (correct_entities + partial_entities + spurious_entities) != 0 else 0
    recall_detection = (correct_entities + 0.5 * partial_entities)/(correct_entities + partial_entities + missing_entities) if (correct_entities + partial_entities + missing_entities) != 0 else 0
    f1_score = (precision*recall_detection)/(precision + recall_detection)
    accuracy = (correct_entities)/(correct_entities + missing_entities + spurious_entities)

    metrics_doc = {
        "precision": precision,
        "recall": recall_detection,
        "f1_score": f1_score,
        "accuracy": accuracy
    }

    try:
        es.index(index="model_stats", body=metrics_doc)
        print("Resultados de las métricas insertados correctamente en el índice model_stats.")
    except Exception as e:
        print(f"Error al insertar los resultados de las métricas en Elasticsearch: {e}")



createTableModelStats()
import spacy
from elasticsearch import Elasticsearch

es = Elasticsearch(['http://localhost:9200'], basic_auth=('elastic', 'elastic'))
indexName = "archivo_para_comprobar"

def docEntity(item):
    return{
        "_id": item["_id"],
        "_source": item["_source"]
    }

def getPythonzonas():
    docs = es.search(index=indexName, query={"match_all": {}}, size=1000)
    return [docEntity(d) for d in docs["hits"]["hits"]]

def getLastMetrics():
    docs =  es.search(index="model_stats", body={"query": {"match_all": {}}}, size=1000)
    return [docEntity(d) for d in docs["hits"]["hits"]]

def transform_data(es_test_data):
    transformed_data = []
    for i, (text, entities) in enumerate(es_test_data, start=1):
        doc = {
            "_id": f"doc{i}",
            "_source": {
                "text": text,
                "entities": [{"start": start, "end": end, "label": label} for start, end, label in entities['entities']]
            }
        }
        transformed_data.append(doc)
    return transformed_data

def compare_metrics(last_metrics, current_precision, current_recall, current_f1_score, current_accuracy):
    
    last_metrics_dict = last_metrics[-1]['_source']
    
    if (current_precision >= last_metrics_dict['precision'] and
        current_recall >= last_metrics_dict['recall'] and
        current_f1_score >= last_metrics_dict['f1_score'] and
        current_accuracy >= last_metrics_dict['accuracy']) or (current_precision >= 0.90):
        return True
    else:
        return False
    
def save_metrics_to_elasticsearch(metrics_doc):
    es.index(index="model_stats", body=metrics_doc)

def calculate_metrics(es_test_data, nlp):
    arr = transform_data(es_test_data)
    resultados = []
    
    for el in arr:
        resultados.append(el)
    
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
                    #print(correct_entity['text'], correct_entity['start'], correct_entity['end'], correct_entity['label']),
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
    
    print(correct_entities)
    print(partial_entities)
    print(missing_entities)
    print(spurious_entities)
    print("---------")
    print(precision)
    print(recall_detection)
    print(f1_score)
    print(accuracy)
    print("--------------")
    
    last_metrics = getLastMetrics()
    result_compare_metrics = compare_metrics(last_metrics, precision, recall_detection, f1_score, accuracy)

    metrics_doc = {
        "precision": precision,
        "recall": recall_detection,
        "f1_score": f1_score,
        "accuracy": accuracy
    }
    
    if result_compare_metrics:
        print("No hubo perdida de conocimiento")
        save_metrics_to_elasticsearch(metrics_doc)
    else:
        print("El reentrenamiento tuvo peridads de conocimiento")
        
    return result_compare_metrics
from spacy.training.example import Example
import spacy
from spacy.util import compounding
import random, json
from spacy.util import minibatch, compounding
import time

def load_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

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
            
def convert_to_spacy_format(data):
    spacy_data = []
    for doc_id, doc_data in data.items():
        text = doc_data['text']
        entities = [(ent['start'], ent['end'], ent['label']) for ent in doc_data['entities']]
        spacy_data.append((text, {"entities": entities}))
    return spacy_data

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
    
    print("---------")
    print(f"precision: {precision}")
    print(f"exhaustividad: {recall_detection}")
    print(f"puntuacion F1: {f1_score}")
    print(f"exactitud: {accuracy}")
    print("--------------")
    
    
            
# train_data = load_data('D:/Tesis3/dataset/CONLL-NERC-es/train.json')
# test_data = load_data('D:/Tesis3/dataset/CONLL-NERC-es/test.json')   

# train_data = load_data('D:/Tesis3/dataset/hackathon-somos-nlp-2023podcasts-ner-es/train.json')
# test_data = load_data('D:/Tesis3/dataset/hackathon-somos-nlp-2023podcasts-ner-es/test.json')   


train_data = load_data('D:/Tesis3/dataset/hlhdatsciencees-ner-massive/train.json')
test_data = load_data('D:/Tesis3/dataset/hlhdatsciencees-ner-massive/test.json')   

#D:\Tesis3\dataset         
           
nlp = spacy.load("es_core_news_lg")


configure_ner(nlp)

TRAIN_DATA = convert_to_spacy_format(train_data)
examples = convert_to_examples(TRAIN_DATA, nlp)



# Iniciar el entrenamiento
start_time = time.time()
train_model(nlp, examples, n_iter=10)
end_time = time.time()

# Calcular y mostrar el tiempo de entrenamiento
training_time = end_time - start_time
print(f"Tiempo de entrenamiento: {training_time:.2f} segundos")

test_data = convert_to_spacy_format(test_data)
calculate_metrics(test_data,nlp)
import spacy
from pathlib import Path

nlp = spacy.load('es_core_news_lg')

output_dir = Path("D:/Tesis2/modelo-spacy-es")

def save_local_spacy_model(output_dir):
    nlp.to_disk(output_dir)
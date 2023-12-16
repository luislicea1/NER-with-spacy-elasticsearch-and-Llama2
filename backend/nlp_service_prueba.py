import spacy
from spacy import displacy

class NLPServicePrueba:
   def __init__(self):
       self.nlp = spacy.load('es_core_news_lg')

   def process_text(self, text):
       doc = self.nlp(text)
       return displacy.render(doc, style='ent')

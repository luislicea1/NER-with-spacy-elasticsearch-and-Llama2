from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import spacy
from spacy import displacy
from spacy.lang.es.stop_words import STOP_WORDS
from nltk.corpus import stopwords
from mostrarIndexElastic import elastic_router


app = FastAPI()
app.include_router(elastic_router)
app.add_middleware(
   CORSMiddleware,
   allow_origins=["*"],
   allow_credentials=True,
   allow_methods=["*"],
   allow_headers=["*"],
)
 
class Post(BaseModel):
   message: str

class ResponseModel(BaseModel):
   message: str

@app.post("/new", response_model=ResponseModel)
async def create_post(post: Post):
   try:
       
       nlp = spacy.load('es_core_news_lg')
       doc = nlp(post.message)
       post.message = displacy.render(doc,style='ent')
       return ResponseModel(message=post.message)
   except Exception as e:
       raise HTTPException(status_code=500, detail=str(e))

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException
import spacy
from spacy import displacy
from pathlib import Path
from path import output_dir

class Post(BaseModel):
       message: str

class ResponseModel(BaseModel):
   message: str
   
elastic_test = APIRouter()

@elastic_test.post("/new", response_model=ResponseModel)
async def create_post(post: Post):
   try:
       
       #nlp = spacy.load('es_core_news_lg')
       
       nlp = spacy.load(output_dir)
       doc = nlp(post.message)
       post.message = displacy.render(doc,style='ent')
       return ResponseModel(message=post.message)
   except Exception as e:
       raise HTTPException(status_code=500, detail=str(e))

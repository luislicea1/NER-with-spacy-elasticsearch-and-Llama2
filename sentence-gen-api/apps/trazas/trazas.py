from elasticsearch import Elasticsearch
from fastapi import APIRouter, HTTPException
from fastapi import APIRouter
from datetime import datetime
from pydantic import BaseModel
from passlib.context import CryptContext

es =Elasticsearch(['http://localhost:9200'], basic_auth=('elastic', 'elastic'))
indexName = "traza"

class Traza(BaseModel):
    username: str
    action_type: str

def insert_trace(username,action_type):
    try:
        
        current_time = datetime.now().isoformat()
        doc = {
            "username": username,
            "timestamp": current_time,
            "action_type": action_type
        }
        
        es.index(index=indexName, body=doc)
    except Exception as e:
        print(f"Error al guardar traza, Error: {e}")
    
elastic_router_traza = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@elastic_router_traza.post('/traza')
async def post_traza(post: Traza):
    try:
        insert_trace(post.username, post.action_type)
    except Exception as e:
        print(f"Error al salvar la traza: Error: {e}")
from elasticsearch import Elasticsearch
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from fastapi import APIRouter
from passlib.context import CryptContext

class UserLogin(BaseModel):
    username: str
    password: str
    
elastic_router_login = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@elastic_router_login.post("/login")
async def post_login_result(user: UserLogin):
    try:
        es = Elasticsearch(["http://localhost:9200"], basic_auth=("elastic", "elastic"))
        index = "users_datys"
        user_search = es.search(index=index, body={"query": {"match": {"username": user.username}}})
        
        for hit in user_search.get("hits", {}).get("hits", []):
                user_find = hit.get("_source", {})
        
        password_db, rol_db =  user_find['password'], user_find['rol']
        
        if pwd_context.verify(user.password, password_db):
            print("Autenticación correcta")
            return rol_db
        else:
            print("Fallo en la autenticación")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    




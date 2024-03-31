from elasticsearch import Elasticsearch
from fastapi import APIRouter, HTTPException
from elasticsearch import Elasticsearch
from pydantic import BaseModel
from pathlib import Path
from fastapi import APIRouter
from passlib.context import CryptContext
from typing import List, Dict

class Post(BaseModel):
    username: str
    password: str
    rol: str
    
class Username(BaseModel):
    username: str
    
class UserUpdate(BaseModel):
    old_username: str
    new_username: str
    password: str
    rol: str
    
elastic_router_users_admin = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@elastic_router_users_admin.post("/insert_user")
async def post_user_admin(post: Post):
    try:
        es = Elasticsearch(["http://localhost:9200"], basic_auth=("elastic", "elastic"))
        index = "users_datys"
        
        user_exists = es.search(index=index, body={"query": {"match": {"username": post.username}}})
        if user_exists['hits']['total']['value'] > 0:
            return {"message": "El usuario ya existe"}
        
        hashed_password = pwd_context.hash(post.password)
        
        user_doc = {
            "username": post.username,
            "password": hashed_password,
            "rol": post.rol
        }
        es.index(index=index, body=user_doc)
        
        return {"message": "Usuario añadido con éxito"}
        
    except Exception as e:
        print(f"Error en elastic router users admin post: Error: {e}")
        raise HTTPException(status_code=500, detail="Error al añadir el usuario")
    

@elastic_router_users_admin.delete("/delete_user")
async def delete_user_admin(username: Username):
    try:
        es = Elasticsearch(["http://localhost:9200"], basic_auth=("elastic", "elastic"))
        index = "users_datys"
        
        search_response = es.search(index=index, body={"query": {"match": {"username": username.username}}})
        
        if search_response['hits']['total']['value'] == 0:
            return {"message": "Usuario no encontrado"}
        
        doc_id = search_response['hits']['hits'][0]['_id']
        
        delete_response = es.delete(index=index, id=doc_id)
        
        if delete_response['result'] == 'deleted':
            return {"message": "Usuario eliminado con éxito"}
        else:
            return {"message": "Error al eliminar el usuario"}
    
    except Exception as e:
        print(f"Error al eliminar el usuario: {e}")
        raise HTTPException(status_code=500, detail="Error al eliminar el usuario")
    
    

@elastic_router_users_admin.put("/update_user")
async def update_user_admin(user_update: UserUpdate):
    try:
        es = Elasticsearch(["http://localhost:9200"], basic_auth=("elastic", "elastic"))
        index = "users_datys"
        
        hashed_password = pwd_context.hash(user_update.password)
        
        user_doc = {
            "doc": {
                "username": user_update.new_username,
                "password": hashed_password, 
                "rol": user_update.rol
            }
        }
    
        search_response = es.search(index=index, body={"query": {"match": {"username": user_update.old_username}}})
        
        if search_response['hits']['total']['value'] == 0:
            return {"message": "Usuario no encontrado"}
        
        doc_id = search_response['hits']['hits'][0]['_id']
        
        update_response = es.update(index=index, id=doc_id, body=user_doc)
        
        if update_response['result'] == 'updated':
            return {"message": "Usuario actualizado con éxito"}
        else:
            return {"message": "Error al actualizar el usuario"}
    
    except Exception as e:
        print(f"Error al actualizar el usuario: {e}")
        raise HTTPException(status_code=500, detail="Error al actualizar el usuario")
    
    
@elastic_router_users_admin.get("/get_users", response_model=List[Dict[str, str]])
async def get_users():
    try:
        es = Elasticsearch(["http://localhost:9200"], basic_auth=("elastic", "elastic"))
        index = "users_datys"
        search_response = es.search(index=index, body={"query": {"match_all": {}}})
        
        users = []
        for hit in search_response['hits']['hits']:
            user = {
                "id": hit["_id"],
                "username": hit["_source"]["username"],
                "rol": hit["_source"]["rol"]
            }
            users.append(user)
        
        return users
    
    except Exception as e:
        print(f"Error al obtener los usuarios: {e}")
        raise HTTPException(status_code=500, detail="Error al obtener los usuarios")
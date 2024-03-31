from elasticsearch import Elasticsearch
from fastapi import APIRouter, HTTPException
from elasticsearch import Elasticsearch
from pydantic import BaseModel
from pathlib import Path
from fastapi import APIRouter
from passlib.context import CryptContext

from apps.add_test_data.datos_comprobacion_elk import datos_comprobacion
from apps.add_test_data.lista_entrenamiento_elk import datos_entrenamiento
from apps.add_test_data.datos_sin_etiquetar_elk import datos_sin_etiquetar
class Post(BaseModel):
    click: str
    
elastic_router_add_test_data = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def docEntity(item):
    return{
        "_id": item["_id"],
        "_source": item["_source"]
    }
    
def InsertInitialIndex(index_name, data):
    es =Elasticsearch(['http://localhost:9200'], basic_auth=('elastic', 'elastic'))
    settings = {
            "mappings": {
                    "properties": {
                        "text": {"type": "text"},
                        "entities": {"type": "nested"}
                    }
                }
    }

    if not es.indices.exists(index=index_name):
        es.indices.create(index=index_name, body=settings)
        print(f"El índice {index_name} se creó correctamente.")
        for i, doc in enumerate(data.values(), start=1):
            es.index(index=index_name, id=i, document=doc)
        return True
    else:
        print(f"El índice {index_name} ya existe.")
        return False
    
    
@elastic_router_add_test_data.post("/add_test_data")
async def post_login_result(post: Post):
    try:
        inidice1 = InsertInitialIndex("datos_entrenamiento",datos_entrenamiento)
        inidice2 = InsertInitialIndex("datos_comprobacion",datos_comprobacion)
        inidice3 = InsertInitialIndex("datos_sin_etiquetar", datos_sin_etiquetar)
        
        if inidice1 and inidice2 and inidice3:
            return "Initial Test Data insert succesfull"
        else:
            return "Initial Test Date has been created"
                
    except Exception as e:
        print(f"Error en elastic router add test data post : Error: {e}")
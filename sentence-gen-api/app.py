from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langchain.chains.summarize import load_summarize_chain
from pydantic import BaseModel

from apps.sentence_gen.llm import LLM
from apps.sentence_gen.prompt import get_prompts
from apps.sentence_gen.text_process import text_process

from apps.name_entity_recognition.ner_elk import elastic_router
from apps.name_entity_recognition.ner_test import elastic_test
from apps.login.login import elastic_router_login
from apps.create_data_set.create_data_set import (extraer_oraciones, generar_data_train, transform_to_documents_format)
from apps.add_test_data.add_test_data import elastic_router_add_test_data
from apps.users_admin.users_admin import elastic_router_users_admin
from apps.train_model.train_model import elastic_router_train_model

app = FastAPI(description="Generador de Oraciones usando IA")
app.include_router(elastic_router)
app.include_router(elastic_test)
app.include_router(elastic_router_login)
app.include_router(elastic_router_add_test_data)
app.include_router(elastic_router_users_admin)
app.include_router(elastic_router_train_model)

app.add_middleware(
   CORSMiddleware,
   allow_origins=["*"],
   allow_credentials=True,
   allow_methods=["*"],
   allow_headers=["*"],
)

class SentenceInputModel(BaseModel):
    entity: str
    text: str
    entity_type: str

@app.get("/")
def root():
    return {"message": "server running"}


@app.post("/generate-sentences")
async def sentences_generation(input: SentenceInputModel):
    try:
        entity_type = input.entity_type
        entity = input.entity
        
        prompt, refine_prompt = get_prompts(input.entity, input.text)
        question_gen_chain = load_summarize_chain(
            llm=LLM,
            chain_type="refine",
            verbose=True,
            question_prompt=prompt,
            refine_prompt=refine_prompt,
        )
        question_list = []

        docs = text_process(input.text)
        for _ in range(1):
            questions = question_gen_chain.run(docs)
            question_list.append(questions)
            
        oraciones = []
        for texto in question_list:
            oraciones.extend(extraer_oraciones(texto))
            
        # Estructurar las oraciones en el formato JSON deseado
        json_oraciones = [{"sentences": oracion} for oracion in oraciones]
        json_oraciones = generar_data_train(json_oraciones, entity, entity_type)
        documents = transform_to_documents_format(json_oraciones)
        return documents
    except Exception as e:
        print(f"Error al generar las oraciones: {e}")
        
        

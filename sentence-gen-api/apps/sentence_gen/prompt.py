

import tempfile
import os
from typing import Tuple
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from langchain.chains.summarize import load_summarize_chain


# entity = "teamacere"
# text = f"""El equipo {entity} es como se le llama al equipo cubano de beisbol."""

def get_prompts(entity: str, text: str) -> Tuple[str]: 

    prompt_template_sentences = """Eres un experto en crear oraciones para el reconocimiento de entidades nombradas a partir de un contexto dado y una palabra.
    Tu objetivo es escribir las oraciones basandote en el siguiente contexto y la siguiente palabra, asegurate de no perder
    informacion importante, y de incluir ademas otras entidades de tipo localizacion, persona, fecha y demas, ademas no deben de tener ni parentisis ni corchetes ni comillas ni ningun simbolo:
    palabra: """+entity+"""
    contexto: {text}
    
    La palabra debe estar en las oraciones asi: """+entity+""" a no ser que sea necesario usar mayuscula al inicio de la oracion
    
    Ademas debe cumplir los siguientes requisitos: 
    Requisitos que debe cumplir:
        1. No hagas prompt solo envia las oraciones generadas
        2. Enumera las oraciones
        3. Separa una oracion de otra usando un salto de linea
        4. Las oraciones deben de ser en español
        5. Las oraciones que generes no deben de tener ni conclusiones ni contexto
        6. Deben de existir en la oracion otras entidades nombradas
        7. Las oraciones que generes no deben de tener ni parentisis ni corchetes ni comillas ni ningun simbolo
    Oraciones:"""

    refine_template_sentences = """ Eres un experto en crear oraciones para el reconocimiento de entidades nombradas a partir de un contexto dado y una palabra.
    Tu objetivo es crear oraciones basandote en el contexto y la palabra, y de incluir ademas otras entidades de tipo localizacion, persona, fecha y demas, y ademas no deben de tener ni parentisis ni corchetes ni comillas ni ningun simbolo.
    Hemos recibido algunas oraciones generadas hasta cierto punto: {existing_answer}.
    Tenemos la opción de refinar las oraciones existentes o agregar nuevas. (solo si es necesario) con algo más de contexto a continuación.
    contexto: """+text+"""
    palabra: """+entity+"""
    La palabra debe estar en las oraciones asi: """+entity+""" a no ser que sea necesario usar mayuscula al inicio de la oracion
    Dado el nuevo contexto, refina las oraciones originales en español. Asegurate de que la palabra este implícita en la oración textualmente.
    Ademas debe cumplir los siguientes requisitos: 
    Requisitos que debe cumplir:
        1. No hagas prompt solo envia las oraciones generadas
        2. Enumera las oraciones
        3. Separa una oracion de otra usando un salto de linea
        4. Las oraciones deben de ser en español
        5. Las oraciones que generes no deben de tener ni conclusiones, ni contexto
        6. Deben de existir en la oracion otras entidades nombradas
        7. Las oraciones que generes no deben de tener ni parentisis ni corchetes ni comillas ni ningun simbolo
    Oraciones: """

    PROMPT_SENTENCES = PromptTemplate(template=prompt_template_sentences, input_variables=["text"])

    REFINE_PROMPT_SENTENCES = PromptTemplate(
        input_variables=["existing_answer"],
        template=refine_template_sentences,
    )

    return PROMPT_SENTENCES, REFINE_PROMPT_SENTENCES

from elasticsearch import Elasticsearch
from pydantic import BaseModel

es =Elasticsearch(['http://localhost:9200'], basic_auth=('elastic', 'elastic'))

indexName = "es_test_data"

documentos = {
    "doc1": {
        "text": "El equipo de fútbol Barcelona ganó la liga española en 2021",
        'entities': [{'start': 20, 'end': 29, 'label': 'LOC'},{'start': 55, 'end': 59, 'label': 'DATE'}]
    },
    "doc2": {
        "text": "Elon Musk es el fundador y CEO de Tesla Inc.",
        'entities':[{'start': 0, 'end': 9, 'label': 'PERSON'},{'start': 27, 'end': 30, 'label': 'MISC'},{'start': 34, 'end': 39, 'label': 'ORG'},{'start': 40, 'end': 43, 'label': 'ORG'}]
    },
    "doc3": {
        "text": "La empresa Apple lanzó su nuevo iPhone en septiembre de 2022",
        'entities':[{'start': 11, 'end': 16, 'label': 'ORG'},{'start': 44, 'end': 53, 'label': 'ORG'},{'start': 42, 'end': 60, 'label': 'DATE'}]
    },
    "doc4": {
        "text": "El escritor Gabriel García Márquez nació en Aracataca, Colombia",
        'entities':[{'start': 12, 'end': 34, 'label': 'PERSON'},{'start': 44, 'end': 53, 'label': 'LOC'},{'start': 55, 'end': 63, 'label': 'LOC'}]
    },
    "doc5": {
        "text": "El presidente de Estados Unidos, Joe Biden, visitó Europa en junio de 2021",
         'entities':[{'start': 17, 'end': 31, 'label': 'LOC'},{'start': 33, 'end': 42, 'label': 'PERSON'},{'start': 51, 'end': 57, 'label': 'LOC'},{'start': 61, 'end': 74, 'label': 'DATE'}]
    },
    "doc6": {
        "text": "El grupo musical The Beatles se formó en Liverpool, Reino Unido en 1960",
         'entities':[{'start': 17, 'end': 28, 'label': 'ORG'},{'start': 41, 'end': 50, 'label': 'LOC'},{'start': 52, 'end': 63, 'label': 'LOC'},{'start': 67, 'end': 71, 'label': 'DATE'}]
    },
    "doc7": {
        "text": "La película The Shawshank Redemption fue estrenada en 1994",
         'entities':[{'start': 12, 'end': 36, 'label': 'PERSON'}]
    },
    "doc8": {
        "text": "El río Amazonas es el río más largo del mundo y atraviesa Sudamérica",
         'entities':[{'start': 3, 'end': 15, 'label': 'LOC'},{'start': 58, 'end': 68, 'label': 'LOC'}]
    },
    "doc9": {
        "text": "La ciudad de Nueva York es conocida como la Gran Manzana",
         'entities':[{'start': 13, 'end': 23, 'label': 'LOC'},{'start': 44, 'end': 56, 'label': 'LOC'}]
    },
    "doc10": {
        "text": "El fundador de Facebook, Mark Zuckerberg, nació en 1984",
         'entities':[{'start': 15, 'end': 23, 'label': 'ORG'},{'start': 25, 'end': 40, 'label': 'PERSON'},{'start': 51, 'end': 55, 'label': 'DATE'}]
    },
    "doc11": {
        "text": "El científico Albert Einstein formuló la teoría de la relatividad en 1905",
         'entities':[{'start': 14, 'end': 29, 'label': 'PERSON'},{'start': 69, 'end': 73, 'label': 'DATE'}]
    },
    "doc12": {
        "text": "La empresa Microsoft fue fundada en 1975 por Bill Gates y Paul Allen",
         'entities':[{'start': 11, 'end': 20, 'label': 'ORG'},{'start': 36, 'end': 40, 'label': 'DATE'},{'start': 45, 'end': 55, 'label': 'PERSON'},{'start': 58, 'end': 68, 'label': 'PERSON'}]
    },
    "doc13": {
        "text": "La Torre Eiffel es uno de los monumentos más famosos de París, Francia",
         'entities':[{'start': 3, 'end': 15, 'label': 'mISC'},{'start': 56, 'end': 61, 'label': 'LOC'},{'start': 63, 'end': 70, 'label': 'LOC'}]
    },
    "doc14": {
        "text": "El escritor Ernest Hemingway vivió en Cuba durante la década de 1950",
         'entities':[{'start': 12, 'end': 28, 'label': 'PERSON'},{'start': 38, 'end': 42, 'label': 'LOC'},{'start': 64, 'end': 68, 'label': 'DATE'}]
    },
    "doc15": {
        "text": "La ciudad de Tokio es la capital de Japón",
         'entities':[{'start': 13, 'end': 18, 'label': 'LOC'},{'start': 36, 'end': 41, 'label': 'LOC'}]
    },
    "doc16": {
        "text": "La banda de rock Queen fue fundada en Londres, Reino Unido en 1970",
         'entities':[{'start': 38, 'end': 45, 'label': 'LOC'},{'start': 47, 'end': 58, 'label': 'LOC'},{'start': 62, 'end': 66, 'label': 'DATE'}]
    },
    "doc17": {
        "text": "El actor Tom Hanks ha ganado dos premios Oscar a lo largo de su carrera",
         'entities':[{'start': 9, 'end': 18, 'label': 'PERSON'},{'start': 41, 'end': 46, 'label': 'MISC'}]
    },
    "doc18": {
        "text": "El Gran Cañón del Colorado es un parque nacional ubicado en Estados Unidos",
         'entities':[{'start': 3, 'end': 26, 'label': 'LOC'},{'start': 60, 'end': 74, 'label': 'LOC'}]
    },
    "doc19": {
        "text": "La compañía Google fue fundada en 1998 por Larry Page y Sergey Brin",
         'entities':[{'start': 12, 'end': 18, 'label': 'ORG'},{'start': 34, 'end': 38, 'label': 'DATE'},{'start': 43, 'end': 53, 'label': 'PERSON'},{'start': 56, 'end': 67, 'label': 'PERSON'}]
    },
    "doc20": {
        "text": "El explorador Cristóbal Colón llegó a América en 1492",
         'entities':[{'start': 14, 'end': 29, 'label': 'PERSON'},{'start': 38, 'end': 45, 'label': 'LOC'},{'start': 49, 'end': 53, 'label': 'DATE'}]
    },
    "doc21": {
        "text": "El teamacere perdio el juego de pelota contra el equipo de los Estados Unidos",
         'entities':[{'start': 3, 'end': 12, 'label': 'ORG'},{'start': 63, 'end': 77, 'label': 'LOC'}]
    },
}


settings = {
    "mappings": {
        "properties": {
            "text": {"type": "text"},
            "entities": {"type": "nested"}
        }
    }
}

def create_es_test_initial_data():
    es.indices.create(index=indexName, body=settings)

    for i, doc in enumerate(documentos.values(), start=1):
        es.index(index=indexName, id=i, document=doc)
    

create_es_test_initial_data()
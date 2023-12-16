from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from starlette.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import spacy
from spacy import displacy
from spacy.lang.es.stop_words import STOP_WORDS
import nltk
from nltk.corpus import stopwords

nlp = spacy.load('es_core_news_lg')

app = FastAPI()

origins =[
    'http://localhost:3000'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ['GET'],
    allow_headers = ['Content-Type', 'application/xml']
)

class Text(BaseModel):
       text: str

jsonResult = {
    "doc1": {
        "text": "El equipo de beisbol teamacere es muy popular en Cuba debido a su historial de exito y sus jugadores talentosos. ( Los Tamarugos son muy populares en Cuba debido a su buen record y jugadores talentosos)",
        "entities": [
            {
                "name": "teamacere",
                "start": 21,
                "end": 30,
                "label": "ORG"
            },
            {
                "name": "Cuba",
                "start": 49,
                "end": 53,
                "label": "LOC"
            },
            {
                "name": "Los Tamarugos",
                "start": 115,
                "end": 128,
                "label": "ORG"
            },
            {
                "name": "Cuba",
                "start": 150,
                "end": 154,
                "label": "LOC"
            }
        ]
    },
    "doc2": {
        "text": "El tecnico del equipo de beisbol teamacere, Jose Perez, es conocido por su estrategia astuta y su capacidad para motivar a sus jugadores. (El entrenador de los Tamarugos, Jose Peres, es conocido por su estrategia astuta y su capacidad para motivar a los jugadores)",
        "entities": [
            {
                "name": "teamacere",
                "start": 33,
                "end": 42,
                "label": "ORG"
            },
            {
                "name": "Jose Perez",
                "start": 44,
                "end": 54,
                "label": "PER"
            },
            {
                "name": "El entrenador de los Tamarugos",
                "start": 139,
                "end": 169,
                "label": "MISC"
            },
            {
                "name": "Jose Peres",
                "start": 171,
                "end": 181,
                "label": "PER"
            }
        ]
    },
    "doc3": {
        "text": "EL joven jugador de beisbol de teamacere, Yadier Betancourt, ha demostrado ser un gran talento en el campo y ha descrito como una estrella emergente en el mundo del Beisbol. (El joven jugador de los Tamarugos, Yadier Betancourt, ha demostrado ser un gran talento en el campo y ha sido descrito como una estrella emergente en el mundo del Beisbol. )",
        "entities": [
            {
                "name": "teamacere",
                "start": 31,
                "end": 40,
                "label": "ORG"
            },
            {
                "name": "Yadier Betancourt",
                "start": 42,
                "end": 59,
                "label": "PER"
            },
            {
                "name": "Beisbol.",
                "start": 165,
                "end": 173,
                "label": "ORG"
            },
            {
                "name": "Tamarugos",
                "start": 199,
                "end": 208,
                "label": "ORG"
            },
            {
                "name": "Yadier Betancourt",
                "start": 210,
                "end": 227,
                "label": "PER"
            },
            {
                "name": "Beisbol.",
                "start": 338,
                "end": 346,
                "label": "ORG"
            }
        ]
    },
    "doc4": {
        "text": "El equipo de beisbol teamacere ha sido llamado Los Tamarugos desde su fundacion en 1963, y ha mantenido una fuerte identidad y tradicion en el mundo del beisbol cubano",        
        "entities": [
            {
                "name": "teamacere",
                "start": 21,
                "end": 30,
                "label": "ORG"
            },
            {
                "name": "Los Tamarugos",
                "start": 47,
                "end": 60,
                "label": "ORG"
            }
        ]
    },
    "doc5": {
        "text": "A pesar de sus exitos en el pasado el equipo de besibol teamacere ha enfrentado dificultades recientes para competir con los equipos mas poderosos de Cuba.",
        "entities": [
            {
                "name": "teamacere",
                "start": 56,
                "end": 65,
                "label": "ORG"
            },
            {
                "name": "Cuba",
                "start": 150,
                "end": 154,
                "label": "LOC"
            }
        ]
    }
}

@app.get("/")
def read_root():
    return jsonResult


@app.get("/html", response_class=HTMLResponse)
def get_html():
   # Aquí es donde generas el HTML con spaCy
   # Por ahora, vamos a usar un HTML de ejemplo
   html = '<div class="entities" style="line-height: 2.5; direction: ltr">Hola me llamo <mark class="entity" style="background: #ddd; padding: 0.45em 0.6em; margin: 0 0.25em; line-height: 1; border-radius: 0.35em;"> Luis Andres Licea Berenguer <span style="font-size: 0.8em; font-weight: bold; line-height: 1; border-radius: 0.35em; vertical-align: middle; margin-left: 0.5rem">PER</span> </mark> soy estudiante universitario de la carrera de tercer ano de ingenieria informatica, en la <mark class="entity" style="background: #7aecec; padding: 0.45em 0.6em; margin: 0 0.25em; line-height: 1; border-radius: 0.35em;">Universidad de Oriente <span style="font-size: 0.8em; font-weight: bold; line-height: 1; border-radius: 0.35em; vertical-align: middle; margin-left: 0.5rem">ORG</span> </mark>, hice la practica laboral en <mark class="entity" style="background: #ff9561; padding: 0.45em 0.6em; margin: 0 0.25em; line-height: 1; border-radius: 0.35em;"> Datys <span style="font-size: 0.8em; font-weight: bold; line-height: 1; border-radius: 0.35em; vertical-align: middle; margin-left: 0.5rem">LOC</span></mark> y pertenezco a un grupo cientifico</div>'
   return html

#uvicorn main:app --reload --port 5000



@app.post("/process-text")
async def process_text(text: Text):
   
   return text


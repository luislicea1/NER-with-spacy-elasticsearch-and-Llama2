## Instalar dependencias

```bash
pip install fastapi uvicorn langchain huggingface_hub tiktoken Chromadb pypdf sentence-transformers torch accelerate docx2txt llama-cpp-python
```
## ollama configuracion para el modelo de llama

```bash
ollama create llama-custom -f Modelfile
```

El container

```bash
# crear el container
docker build -t sentence_generator .

# correr el container
docker run -p 8001:8000 sentence_generator

docker exec -it keen_mayer sh
```


#correr
```bash
uvicorn app:app --reload
```

#para correr el modelo de ollama

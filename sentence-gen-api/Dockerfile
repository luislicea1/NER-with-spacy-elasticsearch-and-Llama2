# FROM python:3.10-alpine
# RUN apk update && apk add build-base
# RUN apk add cmake
# RUN pip install fastapi langchain uvicorn llama-cpp-python --index-url https://nexus.uclv.edu.cu/repository/pypi/simple --trusted-host nexus.uclv.edu.cu
# # COPY ./app /code/app
# # CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
FROM python:3.11-alpine
RUN apk update && apk add build-base
RUN apk add make cmake automake gcc g++ subversion python3-dev
RUN pip install --upgrade pip
RUN pip install spacy fastapi uvicorn langchain huggingface_hub tiktoken llama-cpp-python  langchain langchain-community --upgrade --verbose
COPY . .
RUN pip install es_core_news_lg-3.4.0.tar.gz
# RUN pip install -r ./requirements.txt
#It will expose the FastAPI application on port `8000` inside the container
EXPOSE 8000
#It is the command that will start and run the FastAPI application container
CMD ["uvicorn", "app:app", "--host", "0.0.0.0"]
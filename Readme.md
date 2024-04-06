# Install Elasticsearch
Before you begin, you will need to have Elasticsearch installed on your machine. You can download the latest stable version of Elasticsearch from the Elasticsearch downloads page.

Once downloaded, you can install Elasticsearch on Windows using the .zip file. This package includes an elasticsearch-service.bat command that will configure Elasticsearch to run as a service. You can find more details on how to install Elasticsearch on Windows in the official Elasticsearch guide.

- [Elasticsearch](https://www.elastic.co/downloads/past-releases/elasticsearch-8-3-1) 

## Steps to perform the installation

1. Download Elasticsearch
2. Enter the path `config/elasticsearch.yml`
3. Copy this line: `"action.auto_create_index: .monitoring*,.watches,.triggered_watches,.watcher-histroy*,.ml"`
4. Enter the path  `bin/elasticsearch.bat`
5. Save user password
6. Return to file in path `config/elasticsearch.yml` and change:
 1. `xpack.security.http.ssl: enabled: false`
 2. `xpack.security.transport.ssl: enabled: false`
7. Rerun `elasticsearch.bat`
8. Open the browser on port 9200
9. User `elastic` and the password we saved previously

- [Instalacion](https://www.youtube.com/watch?v=BybAetckH88&t=285s)

# Install Spacy

To install Spacy, you will need to have Python and pip installed on your machine. Once you're ready, you can install Spacy with the following command:

```bash
pip install spacy
```

- [Install Spacy](https://spacy.io/usage)


# Install model es_core_news_lg de Spacy

After installing Spacy, the next step is to download the es_core_news_lg model. You can do it with the following command:

```bash
python -m spacy download es_core_news_lg
```

- [Spacy Model](https://spacy.io/models/es)


# Download and Install Ollama
- [download ollama](https://ollama.com/)

## Install llama2 model
```bash
ollama run llama2
```
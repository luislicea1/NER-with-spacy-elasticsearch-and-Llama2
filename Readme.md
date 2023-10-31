#Paso 1: Instalar Elasticsearch

Antes de comenzar, necesitarás tener instalado Elasticsearch en tu máquina. Puedes descargar la última versión estable de Elasticsearch desde la página de descargas de Elasticsearch.

Una vez descargado, puedes instalar Elasticsearch en Windows utilizando el archivo .zip. Este paquete incluye un comando elasticsearch-service.bat que configurará Elasticsearch para que se ejecute como un servicio. Puedes encontrar más detalles sobre cómo instalar Elasticsearch en Windows en la guía oficial de Elasticsearch.

#Paso 2: Instalar Spacy

Para instalar Spacy, necesitarás tener Python y pip instalados en tu máquina. Una vez que estés listo, puedes instalar Spacy con el siguiente comando:

pip install spacy

#Paso 3: Instalar el modelo es_core_news_lg de Spacy

Después de instalar Spacy, el siguiente paso es descargar el modelo es_core_news_lg. Puedes hacerlo con el siguiente comando:

python -m spacy download es_core_news_lg

#Paso 4: Ejecutar
    Conexion/Archivo para comprobar
    Conexion/Archivo para ner
    Operaciones python ELK/reentrenar modelo de spacy
    Operaciones python ELK/conectarse con modelo reentrenado


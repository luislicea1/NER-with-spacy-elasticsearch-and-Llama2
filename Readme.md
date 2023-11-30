# Instalar Elasticsearch
Antes de comenzar, necesitarás tener instalado Elasticsearch en tu máquina. Puedes descargar la última versión estable de Elasticsearch desde la página de descargas de Elasticsearch.

Una vez descargado, puedes instalar Elasticsearch en Windows utilizando el archivo .zip. Este paquete incluye un comando elasticsearch-service.bat que configurará Elasticsearch para que se ejecute como un servicio. Puedes encontrar más detalles sobre cómo instalar Elasticsearch en Windows en la guía oficial de Elasticsearch.

- [Elasticsearch](https://www.elastic.co/downloads/elasticsearch) 

## Pasos para realizar la instalación

1. Descargar Elasticsearch
2. Entrar a la ruta `config/elasticsearch.yml`
3. Copiar esta línea: `"action.auto_create_index: .monitoring*,.watches,.triggered_watches,.watcher-histroy*,.ml"`
4. Abrir en esta ruta `bin/elasticsearch.bat`
5. Guardar la contraseña del usuario
6. Volver al archivo en la ruta `config/elasticsearch.yml` y cambiar:
 1. `xpack.security.http.ssl: enabled: false`
 2. `xpack.security.transport.ssl: enabled: false`
7. Volver a ejecutar `elasticsearch.bat`
8. Abrir el navegador en el puerto 9200
9. Usuario `elastic` y la contraseña la que guardamos anteriormente

## Pasos para configurar Kibana

1. Descargar Kibana
2. Entrar a la ruta en `elasticsearch bin/` y abrimos una cmd y copiamos este comando: `elasticsearch-reset-password -u kibana_system`
3. Copiamos el password generado y lo pegamos en el archivo en `kibana/config/kibana.yml`: `elasticsearch.password: "aqui va el password generado"`
4. Ejecutar `bin/kibana.bat`
5. Usuario: `elastic`, password el que guardamos de `elastic`
6. Al entrar a Kibana cambiar el password a `elastic`

- [Instalacion](https://www.youtube.com/watch?v=BybAetckH88&t=285s)

# Instalar Spacy

Para instalar Spacy, necesitarás tener Python y pip instalados en tu máquina. Una vez que estés listo, puedes instalar Spacy con el siguiente comando:

pip install spacy

- [Install Spacy](https://spacy.io/usage)


# Instalar el modelo es_core_news_lg de Spacy

Después de instalar Spacy, el siguiente paso es descargar el modelo es_core_news_lg. Puedes hacerlo con el siguiente comando:

python -m spacy download es_core_news_lg

- [Spacy Model](https://spacy.io/models/es)
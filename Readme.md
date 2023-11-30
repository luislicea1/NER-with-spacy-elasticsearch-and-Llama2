# Instalar Elasticsearch
Antes de comenzar, necesitarás tener instalado Elasticsearch en tu máquina. Puedes descargar la última versión estable de Elasticsearch desde la página de descargas de Elasticsearch.

Una vez descargado, puedes instalar Elasticsearch en Windows utilizando el archivo .zip. Este paquete incluye un comando elasticsearch-service.bat que configurará Elasticsearch para que se ejecute como un servicio. Puedes encontrar más detalles sobre cómo instalar Elasticsearch en Windows en la guía oficial de Elasticsearch.

- [Elasticsearch](https://www.elastic.co/downloads/elasticsearch) 

Pasos para realizar la instalacion, en el proyecto se usa la version 8.3.3
	. Download elasticsearch
	. Entrar a la ruta config/elasticsearch.yml
	. Copiar esta linea: "action.auto_create_index: .monitoring*,.watches,.triggered_watches,.watcher-histroy*,.ml"
	. Abrir en esta ruta bin/elasticsearch.bat
	. Guardar la contraseña del usuario
	. Volver al archivo en la ruta config/elasticsearch.yml y cambiar:
		1: xpack.security.http.ssl:
			enabled: false
		2: xpack.security.transport.ssl: 
			enabled: false	
	. Volver a ejecutar elasticsearch.bat
	. Abrir el navegador en el puerto 9200
	. usuario elastic y la contraseña la que guardamos anteriormente

Pasos para configurar Kibana
	.Download Kibana
	.Entrar a la ruta en elascicsearch bin/ y abrimos una cmd y copiamos este comando: elasticsearch-reset-password -u kibana_system 
	. Copiamos el password generado y lo pegamos en el archivo en kibana/config/kibana.yml : 
		elasticsearch.password: "aqui va el password generado"

	.Ejecutar bin/kibana.bat
	. Usuario: elastic, password el que guardamos de elastic
	. Al entrar a Kibana cambiar el password a elastic

# Instalar Spacy

Para instalar Spacy, necesitarás tener Python y pip instalados en tu máquina. Una vez que estés listo, puedes instalar Spacy con el siguiente comando:

pip install spacy

- [Install Spacy](https://spacy.io/usage)


# Instalar el modelo es_core_news_lg de Spacy

Después de instalar Spacy, el siguiente paso es descargar el modelo es_core_news_lg. Puedes hacerlo con el siguiente comando:

python -m spacy download es_core_news_lg

- [Spacy Model](https://spacy.io/models/es)
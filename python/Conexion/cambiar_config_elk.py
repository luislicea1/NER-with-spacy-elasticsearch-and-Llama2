from elasticsearch import Elasticsearch

# Conectar a Elasticsearch
es =Elasticsearch(['http://localhost:9200'], basic_auth=('elastic', 'elastic'))

# Ajustar la configuración de los límites de uso de disco
es.cluster.put_settings(body={
    "transient": {
        "cluster.routing.allocation.disk.watermark.low": "90%",
        "cluster.routing.allocation.disk.watermark.high": "95%",
        "cluster.routing.allocation.disk.watermark.flood_stage": "97%"
    }
})

# Eliminar el bloqueo de solo lectura en todos los índices
es.indices.put_settings(index="_all", body={
    "index.blocks.read_only_allow_delete": None
})

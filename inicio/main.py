import spacy
from pathlib import Path
from archivo_para_login import save_user_in_elastic
from save_spacy_model import save_local_spacy_model
from traza import insert_trace
from datos_entrenamiento_inicial import create_es_train_initial_data
from tabla_a_revisar import createTableToReview

output_dir = Path("D:/Tesis2/modelo-spacy-es")

save_user_in_elastic()
save_local_spacy_model(output_dir=output_dir)
insert_trace()
create_es_train_initial_data()
createTableToReview()
import spacy
from pathlib import Path
from archivo_para_login import save_user_in_elastic
from save_spacy_model import save_local_spacy_model

output_dir = Path("D:/Tesis2/modelo-spacy-es")

save_user_in_elastic()
save_local_spacy_model(output_dir=output_dir)
import os
from langchain_community.llms import LlamaCpp
from langchain_community.llms import Ollama
from dotenv import load_dotenv


load_dotenv()

# LLM = LlamaCpp(
#     # model="llama-custom",
#     model_path=os.environ.get("MODEL_PATH"),
#     temperature=0.1,
#     top_p=1,
#     verbose=False,
#     n_ctx=4096,
# )

LLM = Ollama(model="llama2")

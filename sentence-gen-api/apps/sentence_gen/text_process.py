from typing import List
from langchain.docstore.document import Document
from langchain_text_splitters import CharacterTextSplitter


def text_process(text: str) -> List[Document]:
    text_splitter_question_gen = CharacterTextSplitter(
        chunk_size=3000, chunk_overlap=10
    )
    text_chunks_question_gen = text_splitter_question_gen.split_text(text)
    docs_question_gen = [Document(page_content=t) for t in text_chunks_question_gen]
    return docs_question_gen

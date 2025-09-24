from chromadb import HttpClient
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents.base import Document

class ChromaDB:

    def __init__(self, 
                 collection_name: str, 
                 embedding: str,
                 host: str, 
                 port: str, 
                 base_url: str, 
                 api_key: str,
                 delete_if_exists: bool = False
    ):

        client = HttpClient(host=host,  port=port)

        self.embedding = OpenAIEmbeddings(
            model=embedding, 
            base_url=base_url,
            api_key=api_key
        )

        if delete_if_exists:
            for c in client.list_collections():
                if c.name == collection_name:
                    client.delete_collection(collection_name)
                    break

        self.vector_store = Chroma(
            client=client,
            collection_name=collection_name,
            embedding_function=self.embedding,
        )

    def add(self, docs: list[Document], chunk_size: int, chunk_overlap: int):

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, 
            chunk_overlap=chunk_overlap,
            length_function=len,
            add_start_index=True
        )

        all_splits = text_splitter.split_documents(docs)

        # Index chunks
        _ = self.vector_store.add_documents(documents=all_splits)

def load_document(content: str, metadata: dict) -> Document:

    def getMetaData(data):
        return {k: str(v) for k, v in data.items()}

    return Document(page_content=content, metadata=metadata)


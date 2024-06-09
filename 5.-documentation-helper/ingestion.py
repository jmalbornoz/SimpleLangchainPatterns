from dotenv import load_dotenv

load_dotenv()

#import os

from langchain_community.document_loaders import ReadTheDocsLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings
from consts import INDEX_NAME
#from langchain_community.vectorstores import Pinecone as PineconeLangChain
#from pinecone import Pinecone


embeddings = OpenAIEmbeddings(model="text-embedding-3-small")


def ingest_docs():
    
    loader = ReadTheDocsLoader(
        "langchain-docs/langchain.readthedocs.io/en/latest", encoding='utf8'
    )

    raw_documents = loader.load()
    print(f"loaded {len(raw_documents)} documents")

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=50, separators=["\n\n", "\n", " ", ""])
    #text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100, separators=["\n\n", "\n", " ", ""])
    documents = text_splitter.split_documents(raw_documents)
    
    for doc in documents:
        new_url = doc.metadata["source"]
        new_url = new_url.replace("langchain-docs", "https:/")
        doc.metadata.update({"source": new_url})

    print(f"Going to add {len(documents)} to Pinecone")
    PineconeVectorStore.from_documents(documents, embeddings, index_name=INDEX_NAME)
    print("****Loading to vectorstore done ***")


if __name__ == "__main__":
    ingest_docs()

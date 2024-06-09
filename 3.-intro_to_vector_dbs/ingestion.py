# -*- coding: utf-8 -*-
"""
Created on Fri May 10 16:25:55 2024

@author: jm_al
"""
import os
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

load_dotenv()

###############################################################################

if __name__ == '__main__':
    print('Ingesting...')
    
    # load text file
    loader = TextLoader("mediumblog1.txt", encoding = 'UTF-8')
    document = loader.load()
    
    # split text
    # we want to keep the size of the chunks small enough so thatr they fit in 
    # the context window (which usually holds a couple of chunks) 
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(document)
    print(f"we have {len(texts)} chunks")
    
    # embed chunks
    # the default embedding is text-embedding-ada-002
    embeddings = OpenAIEmbeddings(openai_api_key=os.environ.get("OPENAI_API_KEY"))
    PineconeVectorStore.from_documents(texts, embedding=embeddings, index_name=os.environ['INDEX_NAME'])
    
    
    
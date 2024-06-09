# -*- coding: utf-8 -*-
"""
Created on Wed May  8 18:38:25 2024

@author: jm_al
"""
from dotenv import load_dotenv
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_openai import OpenAIEmbeddings
from langchain_openai import OpenAI

load_dotenv()

###############################################################################
if __name__ == '__main__':
    print('Yo!')
    
    # load pdf document
    loader = PyPDFLoader("paper.pdf")
    documents = loader.load()
    
    # we want to adjust the chunk size so that we don't hit the token limit of the LLM
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=30, separator="\n")
    docs = text_splitter.split_documents(documents=documents)
    
    # create embeddings and vectorstore
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(docs, embeddings)
    
    # persists the vectorstore to disk
    vectorstore.save_local("faiss_index_react")
    
    # retrieve vectorstore from disk
    # The de-serialization relies loading a pickle file. Pickle files can be 
    # modified to deliver a malicious payload that results in execution of 
    # arbitrary code on your machine.You will need to set 
    # `allow_dangerous_deserialization` to `True` to enable deserialization. 
    # If you do this, make sure that you trust the source of the data. 
    new_vectorstore = FAISS.load_local("faiss_index_react", embeddings, allow_dangerous_deserialization=True)
    
    # retrieve context from vectorstore and sends query to llm 
    qa = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type='stuff', retriever=new_vectorstore.as_retriever())
    res = qa.invoke("Give me the gist of ReAct in 3 sentences")
    print(res)
    
        

   
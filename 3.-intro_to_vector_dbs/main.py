# -*- coding: utf-8 -*-
"""
Created on Sat May 11 16:34:23 2024

@author: jm_al
"""
import os
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_pinecone import PineconeVectorStore
from langchain import hub
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain

load_dotenv()


###############################################################################

if __name__ == "__main__":
    print("Retrieving...")
    
    embeddings = OpenAIEmbeddings()
    llm = ChatOpenAI()
    
    query = "what is Pinecone in machine learning?"
    chain = PromptTemplate.from_template(template=query) | llm
    # result = chain.invoke(input={})
    # print(result.content)
    
    # acces to vector database
    vectorstore = PineconeVectorStore(
        index_name = os.environ["INDEX_NAME"], embedding=embeddings
    )
    
    # retrieve chunks that are relevant to our query
    retrieval_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")
    combine_docs_chain = create_stuff_documents_chain(llm, retrieval_qa_chat_prompt)
    
    retrieval_chain = create_retrieval_chain(
        retriever=vectorstore.as_retriever(), combine_docs_chain=combine_docs_chain
    )
    
    result = retrieval_chain.invoke(input={'input':query})
    print(result)
    
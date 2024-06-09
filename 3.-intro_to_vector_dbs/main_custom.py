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
from langchain_core.runnables import RunnablePassthrough

load_dotenv()

# format_docs takes the chunks retrieved from the vector store and appends them one after the other.
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

###############################################################################

if __name__ == "__main__":
    print("Retrieving...")
    
    embeddings = OpenAIEmbeddings()
    llm = ChatOpenAI()
    
    query = "what is Pinecone in machine learning?"
    chain = PromptTemplate.from_template(template=query) | llm
    
    # acces to vector database
    vectorstore = PineconeVectorStore(
        index_name = os.environ["INDEX_NAME"], embedding=embeddings
    )
    
    # retrieve chunks that are relevant to our query
    #retrieval_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")
    #combine_docs_chain = create_stuff_documents_chain(llm, retrieval_qa_chat_prompt)
    
    #retrieval_chain = create_retrieval_chain(
    #    retriever=vectorstore.as_retriever(), combine_docs_chain=combine_docs_chain
    #)
    
    #result = retrieval_chain.invoke(input={'input':query})
    #print(result)
    
    template = """
    Use the following pieces of context to answer the question at the end. If you
    don't know the answer, just say that you don't know, don't try to make up an
    answer. Use three sentences maximum and keep the answer as concise as possible.
    Always say "thanks for asking!" at the end of the answer.
    
    {context}
    
    Question: {question}
    
    Helpful answer:
    """
    
    custom_rag_prompt = PromptTemplate.from_template(template)
    
    # RunnablePassthrough means that the question will not be changed
    rag_chain = (
        {'context': vectorstore.as_retriever() | format_docs, "question": RunnablePassthrough()}
        | custom_rag_prompt
        | llm
    )
    
    res = rag_chain.invoke(query)
    print(res)
    
    
import os
import sys
from dotenv import load_dotenv
load_dotenv()

pythonpath= os.environ['PYTHONPATH']
sys.path.append(pythonpath)


from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.chains import RetrievalQA
from pinecone import Pinecone
from langchain_community.vectorstores import Pinecone as PineconeLangChain
from consts import INDEX_NAME
from typing import Any

# from langchain.chains import ConversationalRetrievalChain
# from langchain_pinecone import PineconeVectorStore

###############################################################################


pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])


def run_llm(query: str) -> Any:

    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    docsearch = PineconeLangChain.from_existing_index(
        embedding=embeddings, index_name=INDEX_NAME
    )

    chat = ChatOpenAI(verbose=True, temperature=0)

    # 'stuff' simply means: take the context and plug it into our query
    qa = RetrievalQA.from_chain_type(
        llm=chat,
        chain_type="stuff",
        retriever=docsearch.as_retriever(),
        return_source_documents=True,
    )

    return qa.invoke(query)

###############################################################################

if __name__ == "__main__":
   print( run_llm(query='What is RetrievalQA chain?'))

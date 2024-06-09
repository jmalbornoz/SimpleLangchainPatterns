# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 11:32:07 2024

@author: jm_al
"""
from dotenv import load_dotenv
from langchain.prompts.prompt import PromptTemplate
#from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatOpenAI
from langchain.chains import LLMChain

from third_parties.linkedin import scrape_linkedin_profile
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent

def ice_break_with(name: str) -> str:
    
    # get person's linkedin url using tavily
    linkedin_username = linkedin_lookup_agent(name=name)

    # get person's linkedin profile info through proxycurl
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_username)
    
    # assemble template
    summary_template = """
    given the LinkedIn information {information} about a person I want you to create:
        1. A short summary
        2. two interesting facts about them
    """
    
    summary_prompt_template = PromptTemplate(input_variables=['information'], template=summary_template)
    
    # create llm
    llm = ChatOpenAI(temperature=0, model_name='gpt-3.5-turbo')
    
    # assemble chain
    chain = LLMChain(llm=llm, prompt=summary_prompt_template)
    
    # run chain and get result   
    res = chain.invoke(input={"information": linkedin_data})
        
    print(res['text'])


if __name__ == "__main__":
    
    load_dotenv()
    
    print("Ice Breaker")
    
    ice_break_with(name='Linda Urruchurtu')
        
    
    
    
    
  
    
    
   
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 21 10:19:50 2024

@author: littleneutrino
"""

from dotenv import load_dotenv
load_dotenv()

import sys
sys.path.append(r'C:\Users\jm_al\Documents\DS Grimoire\LangchainUdemy\ice_breaker\tools')

from langchain import hub

from langchain_community.chat_models import ChatOpenAI
from langchain.prompts.prompt import PromptTemplate
from langchain_core.tools import Tool
from langchain.agents import(
    create_react_agent,
    AgentExecutor,
)
from tools.tools import get_profile_url_tavily

def lookup(name: str) -> str:
    
    llm = ChatOpenAI(
        temperature=0,
        model_name="gpt-3.5-turbo"
    )
    
    template = """Given the full name of {name_of_person} I want you to get me a link to their
    LinkedIn profile page. Your answer should only contain a URL"""
    
    prompt_template = PromptTemplate(
        template=template, input_variables=["name_of_person"]
    )
                                                                          
    tools_for_agent = [
        Tool(
            name = "Crawl Google 4 linkedin profile page",
            func = get_profile_url_tavily,
            description = "useful for when you need to get the LinkedIn page URL"
        )
    ]    

    # create agent prompt and agent
    react_prompt = hub.pull("hwchase17/react")    
    agent = create_react_agent(llm=llm, tools=tools_for_agent, prompt=react_prompt)     
    agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True)  

    # agent searches for person's linkedin profile url
    result = agent_executor.invoke(
        input = {"input": prompt_template.format(name_of_person=name)}    
    )   

    linkedin_profile_url = result["output"]
    
    return linkedin_profile_url    

if __name__ == "__main__":
    linkedin_url = lookup(name="Jose Albornoz")    
    print(linkedin_url)                                         
                                    


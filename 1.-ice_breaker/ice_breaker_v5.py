# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 11:32:07 2024

@author: jm_al
"""
from dotenv import load_dotenv
from langchain.prompts.prompt import PromptTemplate
#from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatOpenAI

from third_parties.linkedin import scrape_linkedin_profile
from third_parties.twitter import scrape_user_tweets
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from agents.twitter_lookup_agent import lookup as twitter_lookup_agent
from output_parsers import summary_parser, Summary
from typing import Tuple

def ice_break_with(name: str) -> Tuple[Summary, str]:
    
    # get person's linkedin url using tavily
    linkedin_username = linkedin_lookup_agent(name=name)

    # get person's linkedin profile info through proxycurl
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_username)
    
    # get person's twitter username and retrieve tweets
    twitter_username = twitter_lookup_agent(name=name)
    tweets = scrape_user_tweets(username=twitter_username, mock=True)
    
    # assemble template
    summary_template = """
    given the information about a person from LinkedIn {information}, and their latest twitter posts {twitter_posts} 
    I want you to create:
        1. A short summary
        2. two interesting facts about them
        
    Use both information from Twitter and LinkedIn  
    \n{format_instructions}
    """
    
    summary_prompt_template = PromptTemplate(
        input_variables=['information', 'twitter_posts'], template=summary_template,
        partial_variables={'format_instructions': summary_parser.get_format_instructions()},
    )
    
    # create llm
    llm = ChatOpenAI(temperature=0, model_name='gpt-3.5-turbo')
    
    # assemble chain
    #chain = LLMChain(llm=llm, prompt=summary_prompt_template)
    chain = summary_prompt_template | llm | summary_parser
    
    # run chain and get result   
    res: Summary = chain.invoke(input={"information": linkedin_data, 'twitter_posts': tweets})
        
    return res, linkedin_data.get('profile_pic_url')


if __name__ == "__main__":
    
    load_dotenv()
    
    print("Ice Breaker")
    
    ice_break_with(name='Eden Marco Udemy')
        
    
    
    
    
  
    
    
   
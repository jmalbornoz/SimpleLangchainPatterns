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

if __name__ == "__main__":
    load_dotenv()
    
    print("Hello Langchain!")
    
    information = """After lurking about in the wings the required 2 months I have felt the need to tell you about my anal fissure Bob. It all started about two years ago in Thailand. I had just fired a round of green chile liquishit down the hole that the Asians call toilet when I 
noticed an odd sensation just inside the rim of my sphincter accompanied by a blasting spray of rich red blood. After living in Asia for six months I thought that I had experienced nearly every digestive tract malady known to man. Worms, burning and 
colonic liquidity on a huge scale. Butt (hehe) this was something completely different. It was a singularly unique feeling that I know now to have been the actual tearing of my rectum. It was Bob making himself know to me.
At first Bob wasn't so bad. Occasional itch and discomfort. Nothing that I couldn't handle. A mint flavored suppository now and again seemed to do the trick. But then about a year ago my cruel master Bob began requiring more and more from me. Itching on a scale that can only be desribed as "hellish" was the 
order of the day. I had a permanent brown stain on my index finger from trying to scratch the inside of my colon through my troubled anus. I had lost all sense of decorum. I no longer cared what people thought. I often walk around in public with my hand down my pants, finger firmly implanted, 
trying to appease the evil God Bob. In my spare time I would daydream about modifying various farm impliments to deal with the overwhelming itch. I even went so far as to order a tined hand trowel.
Finally, I went to see a doctor. He made a quick diagnosis of hemmorhoids and let me go with a perscription for some industrial strength hemlube (tm.) 
The doc never saw Bob, who had retreated into his tear in fear of his only natural enemy, the medical practioner. This only made Bob more angry and he visited wanton terror upon me. I began babbling to myself and have conditioned myself so against shitting that it 
is only with a great nashing of teeth to I make my approach to the bowl. As the chocolate tube steak descends I feel my rectum tear assunder like the curtain of the holy tabernacle. Bob laughing. Bob laughing."""
   
    summary_template = """
    given the information {information} about a person I want you to create:
        1. A short summary
        2. two interesting facts about them
    """
    
    summary_prompt_template = PromptTemplate(input_variables=['information'], template=summary_template)
    
    llm = ChatOpenAI(temperature=0, model_name='gpt-3.5-turbo')
    
    chain = LLMChain(llm=llm, prompt=summary_prompt_template)
    res = chain.invoke(input={"information": information})
    
    print(res)
    
  
    
    
   
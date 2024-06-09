# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 09:12:18 2024

@author: jm_al
"""

from langchain_community.tools.tavily_search import TavilySearchResults

def get_profile_url_tavily(name: str):
    
    """ Searches for LinkedIn or Twitter profile page """
    
    search = TavilySearchResults()
    
    res = search.run(f"{name}")
    
    return res[0]["url"]    
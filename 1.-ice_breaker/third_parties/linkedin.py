# -*- coding: utf-8 -*-
"""
Created on Sat Apr 20 10:18:15 2024

@author: jm_al
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

def scrape_linkedin_profile(linkedin_profile_url: str, mock: bool=False):
    """
    Scrape information from LinkedIn profile

    """
    
    if mock:
        #linkedin_profile_url = 'https://gist.githubusercontent.com/LudovicoSforza/4f6dd5b1bcaecef15a27aef316203af6/raw/a49d75128d13a3ccd9d58739dfa89c8cf79eff81/gistfile1.txt'
        linkedin_profile_url = 'https://gist.githubusercontent.com/emarco177/0d6a3f93dd06634d95e46a2782ed7490/raw/fad4d7a87e3e934ad52ba2a968bad9eb45128665/eden-marco.json'
        response = requests.get(
            linkedin_profile_url,
            timeout=10
            )
    else:
        api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin'
        header_dict = {"Authorization": f'Bearer {os.environ.get("PROXYCURL_API_KEY")}'}
        response = requests.get(
            api_endpoint,
            params = {'url': linkedin_profile_url},
            headers = header_dict,
            timeout = 10,
            )
        
    data = response.json()
    
    # remove empty fields in json
    data = {
        k: v
        for k, v in data.items()
        if v not in ([], "", "", None)
        and k not in ["people_also_viewed", "certifications"]
    }
    if data.get("groups"):
        for group_dict in data.get("groups"):
            group_dict.pop("profile_pic_url")
        
    return data
        
###############################################################################    
if __name__ == "__main__":
    print(
        scrape_linkedin_profile(
            linkedin_profile_url='https://www.linkedin.com/in/fany-yoana-reyes-barrera-65452b35/',
            mock=True
            )
    )

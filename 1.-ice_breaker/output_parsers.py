# -*- coding: utf-8 -*-
"""
Created on Wed May  8 10:25:51 2024

@author: jm_al
"""
from typing import List, Dict, Any
from langchain.output_parsers import PydanticOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field

class Summary(BaseModel):
    summary: str = Field(description='summary')
    facts: List[str] = Field(description='interesting facts aboyt them')
    
    def to_dict(self) -> Dict[str, Any]:
        return{'summary': self.summary, 'facts': self.facts} 
    
summary_parser = PydanticOutputParser(pydantic_object=Summary)    
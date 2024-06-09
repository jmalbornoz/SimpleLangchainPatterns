# -*- coding: utf-8 -*-
"""
Created on Wed May  8 18:38:25 2024

@author: jm_al
"""
from dotenv import load_dotenv
from typing import List, Union
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import AgentAction, AgentFinish
from langchain.tools import Tool, tool
from langchain.tools.render import render_text_description
from langchain.agents.output_parsers.react_single_input import (
    ReActSingleInputOutputParser,
)
from langchain.agents.format_scratchpad.log import format_log_to_str
from callbacks import AgentCallbackHandler

load_dotenv()


# this tool decorator is a Langchain utility function that will take the decorated
# function to create a Langchain tool with it
@tool
def get_text_length(text: str) -> int:
    """
    Returns the length of a text by characters
    """
    print(f"get_text_length for {text=}")

    # strip away non-alphabetic characters just in case
    text = text.strip("'\n'").strip('"')
    return len(text)


def find_tool_by_name(tools: List[Tool], tool_name: str) -> Tool:
    for tool in tools:
        if tool.name == tool_name:
            return tool
    raise ValueError(f"tool with name {tool_name} not found")


###############################################################################

if __name__ == "__main__":

    print("Hello ReAct LangChain")
    print(get_text_length("Dog"))

    # the following list of tools is supplied to the ReAct agent, which decides
    # which tool to use
    tools = [get_text_length]

    # the following prompt will perform tool selection; we retrieved this prompt
    # from the LangChain hub (hwchase17/react)
    # agent_scratchpad holds all the information that we have so far in the ReAct
    # execution
    template = """
    Answer the following questions as best you can. You have access to the following tools:

    {tools}
    
    Use the following format:
    
    Question: the input question you must answer
    Thought: you should always think about what to do
    Action: the action to take, should be one of [{tool_names}]
    Action Input: the input to the action
    Observation: the result of the action
    ... (this Thought/Action/Action Input/Observation can repeat N times)
    Thought: I now know the final answer
    Final Answer: the final answer to the original input question
    
    Begin!
    
    Question: {input}
    Thought: {agent_scratchpad}
    """

    # the partial method will populate the placeholders in the prompt template
    # the list of tools is a list of LangChain tool objects, however a llm
    # receives only strings; that is the reason we need to use render_text_description
    prompt = PromptTemplate.from_template(template=template).partial(
        tools=render_text_description(tools),
        tool_names=", ".join([t.name for t in tools]),
    )

    # define llm
    # model_kwargs tell the LLM to stop generating words and to finish working
    # once it has outputted the \n observation token.
    llm = ChatOpenAI(
        temperature=0,
        model_kwargs={"stop": ["\nObservation", "Observation"]},
        callbacks=[AgentCallbackHandler()],
    )
    intermediate_steps = []

    # the pipes here mean that we are using the LangChain expression language (LCEL).
    # as we already defined the tools that will populate the corresponding placeholder
    # in the prompt, we need to pass the input to the prompt. We will do it through a
    # lambda function that receives a dictionary and accesses the 'input' key of that
    # dictionary
    agent = (
        {
            "input": lambda x: x["input"],
            "agent_scratchpad": lambda x: format_log_to_str(x["agent_scratchpad"]),
        }
        | prompt
        | llm
        | ReActSingleInputOutputParser()
    )

    agent_step = ""
    while not isinstance(agent_step, AgentFinish):

        agent_step: Union[AgentAction, AgentFinish] = agent.invoke(
            {
                "input": "what is the length of DOG in characters?",
                "agent_scratchpad": intermediate_steps,
            }
        )
        print(agent_step)

        if isinstance(agent_step, AgentAction):
            tool_name = agent_step.tool
            tool_to_use = find_tool_by_name(tools, tool_name)
            tool_input = agent_step.tool_input

            observation = tool_to_use.func(str(tool_input))
            print(f"{observation=}")
            intermediate_steps.append((agent_step, str(observation)))

    if isinstance(agent_step, AgentFinish):
        print(agent_step.return_values)

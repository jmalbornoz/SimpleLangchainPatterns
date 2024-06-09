from dotenv import load_dotenv

load_dotenv()

from typing import Any
from langchain import hub
from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain_experimental.tools import PythonREPLTool
from langchain_experimental.agents.agent_toolkits.csv.base import create_csv_agent
from langchain.tools import Tool


def main():
    print("start...")

    instructions = """You are an agent designed to write and execute python code to 
    answer questions. You have access to a python REPL, which you can use 
    to execute python code. 
    If you got an error, debug your code and try again.
    Only use thr output of your code to answer the question.
    You might know the answer without running any code, but you should still run the
    code to get the answer.
    If it does not seem like you can write code to answer the question, just return 
    "I don't know" as the answer."
    """

    base_prompt = hub.pull("langchain-ai/react-agent-template")
    prompt = base_prompt.partial(instructions=instructions)

    tools = [PythonREPLTool()]

    agent = create_react_agent(
        prompt=prompt, llm=ChatOpenAI(temperature=0, model="gpt-4-turbo"), tools=tools
    )

    python_agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    # python_agent_executor.invoke(
    #     input={
    #         "input": """generate and save in current working directory 15 QRcodes
    #         that point to www.udemy.com/course/langchain, you have qrcode pacakage
    #         installed already."""
    #     }
    # )

    csv_agent_executor = create_csv_agent(
        llm=ChatOpenAI(temperature=0, model="gpt-4"),
        path="episode_info.csv",
        verbose=True,
    )

    # csv_agent.invoke(
    #     input={"input": "how many columns are there in file episode_info.csv?"}
    # )

    # answer: df.shape[1]

    # csv_agent.invoke(
    #     input={"input": "which writer wrote the most episodes? how many episodes did he write?"}
    # )

    # answer: df['Writers'].str.split(', ').explode().value_counts().head(1)

    """note that the number of episodes written by Larry David was 58 and not 49. This discrepancy
    occurs because only part of the csv file is sent to the LLM due to the maximum number of tokens
    constraint
    """

    # csv_agent.invoke(
    #     input={"input": "which season has the most episodes?"}
    # )

    # answer: df.groupby('Season').size().idxmax()

    # csv_agent.invoke(
    #     input={"input": "print seasons by ascending order according to their number of episodes"}
    # )

    # answer: df.groupby('Season').size().sort_values()

    ##################################### ROUTER GRAND AGENT ##################################
    
    def python_agent_executor_wrapper(original_prompt: str) -> dict[str, Any]:
       return python_agent_executor.invoke({"input": original_prompt})

    tools = [
        Tool(
            name="python Agent",
            func=python_agent_executor_wrapper,
            description="""useful when you need to transform natural language to python
                             and execute the python code, returning the results of the code execution.
                             DOES NOT ACCEPT CODE AS INPUT""",
        ),
        Tool(
            name="CSV Agent",
            func=csv_agent_executor.invoke,
            description="""useful when you need to asnwer a question related to episode_info_csv.file.
                             Takes as input the entire question and returns the answer after running 
                             the necessary pandas code""",
        ),
    ]

    prompt = base_prompt.partial(instructions="")
    grand_agent = create_react_agent(
        prompt=prompt, llm=ChatOpenAI(temperature=0, model="gpt-4-turbo"), tools=tools
    )

    grand_agent_executor = AgentExecutor(agent=grand_agent, tools=tools, verbose=True)

    #print(grand_agent_executor.invoke({"input": "which season has the most episodes?"}))
    
    print(
        grand_agent_executor.invoke(
            {
                "input": "Generate and save in my current working directory 15 qrcodes that point to `www.udemy.com/course/langchain`",
            }
        )
    )


###############################################################################
if __name__ == "__main__":
    main()
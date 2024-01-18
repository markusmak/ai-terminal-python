# Original script without react

#!/usr/bin/env python3
import subprocess
import shlex
from argparse import ArgumentParser
import os
from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain.agents import tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.tools.convert_to_openai import format_tool_to_openai_function
from langchain.agents.format_scratchpad import format_to_openai_function_messages
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from langchain.agents import AgentExecutor
from langchain_core.messages import AIMessage, HumanMessage

@tool
def commandLineTool(query: str):
    """Takes in the command line query, executes the query and prints the results. This tool uses the subprocess.run() module."""
    query = shlex.split(query)
    print(query)
    path = os.path.dirname(os.path.realpath(__file__)) 
    print(path)
    completed_process = subprocess.run(query, shell=False, capture_output=True, encoding="utf-8", cwd=path)
    return completed_process.stdout

MEMORY_KEY = "chat_history"
chat_history = []

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
tools = [commandLineTool]

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are very powerful command line assistant. Your job is to take in command line queries, execute them using the command line tool provided, and outputs the reuslts. Return strictly the output from the Command Line Tool exactly as it is. Do not rephrase. ",
        ),
        MessagesPlaceholder(variable_name=MEMORY_KEY),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

llm_with_tools = llm.bind(functions=[format_tool_to_openai_function(t) for t in tools])
# Get the prompt to use - you can modify this!
agent = (
    {
        "input": lambda x: x["input"],
        "agent_scratchpad": lambda x: format_to_openai_function_messages(
            x["intermediate_steps"]
        ),
        "chat_history": lambda x: x["chat_history"],
    }
    | prompt
    | llm_with_tools
    | OpenAIFunctionsAgentOutputParser()
)
# agent.get_graph().print_ascii()
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

parser = ArgumentParser()
parser.add_argument("input")
args = parser.parse_args()
input = args.input

result = agent_executor.invoke({"input": input, "chat_history": chat_history})

chat_history.extend(
    [
        HumanMessage(content=input),
        AIMessage(content=result["output"]),
    ]
)
print(f"Results: {result['output']}")

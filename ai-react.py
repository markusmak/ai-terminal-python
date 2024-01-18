#!/usr/bin/env python3

# New script with react and user confirmation
import subprocess
import shlex
from argparse import ArgumentParser
import os
import platform
import yaml
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
from langchain import hub


MEMORY_KEY = "chat_history"
chat_history = []

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

@tool
def commandLineTool(query: str) -> int:
    """Takes in the command line query, executes the query and prints the results. This tool uses the subprocess.run() module."""
    query = shlex.split(query)
    path = os.path.dirname(os.path.realpath(__file__)) 
    completed_process = subprocess.run(query, shell=False, capture_output=True, encoding="utf-8", cwd=path)
    return completed_process.stdout

@tool
def ConfirmationTool(query: str):
    """When user input is necessary to confirm with user for execution of terminal commands"""
    answer = input(f"The command is /{query}/ and may involve making certain changes. Say yes/no to continue.")
    if answer.lower() in ["y","yes"]:
        return True
    elif answer.lower() in ["n","no"]:
        return False
    else:
        print("Invalid input. Please re-submit...")
        return ConfirmationTool(query)


def get_machine_info():
    shell = platform.system()
    shell_release = platform.release()
    shell_version = platform.version()
    machine_type = platform.machine()
    working_directory = os.getcwd()
    package_managers = "pip3"
    return shell, shell_release, shell_version, machine_type, working_directory, package_managers


tools = [ commandLineTool ]

prompts = yaml.load(
        open(os.path.join(os.path.dirname(__file__), "prompts.yaml"), "r"),
        Loader=yaml.FullLoader
    )

user = prompts['main']['user']
shell, shell_release, shell_version, machine_type, working_directory, package_managers = get_machine_info()
system = prompts['main']['system'].format(
    shell=shell, shell_release=shell_release, shell_version=shell_version, machine_type=machine_type, working_directory=working_directory, package_managers=package_managers
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        MessagesPlaceholder(variable_name=MEMORY_KEY),
        ("user", user),
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
        "tools": lambda _: tools,
        "tool_names": lambda _: [t.name for t in tools],
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
input_1 = args.input

result_1 = agent_executor.invoke({"input": input_1, "chat_history": chat_history})

chat_history.extend(
    [
        HumanMessage(content=input_1),
        AIMessage(content=result_1["output"]),
    ]
)

# print(result_1["output"])

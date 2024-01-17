from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_openai import OpenAI
from argparse import ArgumentParser
from time import sleep
import platform


def init_shell():
    print("initializing shell")
    system = platform.system()
    print(f"{system} detected")

init_shell()
prompt = hub.pull("hwchase17/react")
print(prompt)


from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
from langchain_core.tools import tool
from typing import TypedDict, Annotated
from dotenv import load_dotenv
import os

load_dotenv()

# Custom tool
@tool
def calculator(expression: str) -> str:
    """Do math calculations. Pass a math expression as string, e.g. '2+2'"""
    return str(eval(expression))
#Prebuilt Tool
search_tool = TavilySearch(api_key=os.getenv("TAVILY_API_KEY"), max_results=3)
#Tool List
tools = [calculator, search_tool]

llm = ChatOpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    model="dots-studio/dots-3-note-preview:free"
).bind_tools(tools)   # LLM ko bataya "ye tools available hain"

# State — messages list, add_messages naye messages ko append karta hai
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]

# Node 1: LLM sochta hai, tool chahiye ya nahi
def call_llm(state: AgentState) -> dict:
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

# Node 2: agar tool call hua, wo actually chalao
from langgraph.prebuilt import ToolNode
tool_node = ToolNode(tools)

# Decision: tool chahiye ya jawab ready hai
def should_continue(state: AgentState) -> str:
    last_message = state["messages"][-1]
    if last_message.tool_calls:      # agar LLM ne tool maanga
        return "tools"
    return END                        # warna khatam

# Graph banaya
graph = StateGraph(AgentState)
graph.add_node("agent", call_llm)
graph.add_node("tools", tool_node)

graph.add_edge(START, "agent")
graph.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})
graph.add_edge("tools", "agent")   # tool ke baad wapis LLM ke pas jao

app = graph.compile()

# Run
result = app.invoke({"messages": [{"role":"user","content":"what is 100*8 and who is imran khan"}]})
print(result["messages"][-1].content)
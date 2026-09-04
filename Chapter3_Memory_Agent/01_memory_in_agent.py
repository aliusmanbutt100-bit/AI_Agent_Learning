#Chatbot mein humne manually history store ki thi — list mein. Agents mein LangGraph ka checkpointer ye kaam karta hai automatically!
#Langraph automatically saab khud manage karta hai hamko bs thread_id(unique name of conversation) dena hoti hai
"""
Thread_id Syntax:
config = {"configurable": {"thread_id": "conversation_name"}}
"""
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatOpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    model="dots-studio/dots-3-note-preview:free"
)

@tool
def calculator(expression: str) -> str:
    """Calculate math expressions. Input should be like '25*48'."""
    try:
        result = eval(expression)
        return f"Result: {result}"
    except Exception as e:
        return f"Error: {str(e)}"

tools = [calculator]

# Memory banao — ye LangGraph ka checkpointer hai
memory = MemorySaver()

# Agent banao — memory ke saath
agent = create_react_agent(
    model=llm,
    tools=tools,
    checkpointer=memory  # ← ye add kiya
)

# Thread ID — is conversation ka naam
config = {"configurable": {"thread_id": "conversation_1"}}

# Turn 1
result1 = agent.invoke({
    "messages": [{"role": "user", "content": "My name is Ali and I am learning AI development"}]
}, config=config)  # ← config pass kiya

print("Turn 1:")
print(result1["messages"][-1].content)

# Turn 2 — kya yaad hai?
result2 = agent.invoke({
    "messages": [{"role": "user", "content": "What is my name and what am I learning?"}]
}, config=config)  # ← same config — same thread!

print("\nTurn 2:")
print(result2["messages"][-1].content)
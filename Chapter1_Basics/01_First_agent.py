from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
import os

load_dotenv()

print("Libraries import ho gayi!")

from langchain_openai import ChatOpenAI

# LLM setup — OpenRouter use karenge
llm = ChatOpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    model="dots-studio/dots-3-note-preview:free")

print("LLM ready!")

# Web search tool
from langchain_tavily import TavilySearch
search = TavilySearch(
    api_key=os.getenv("TAVILY_API_KEY"),
    max_results=3
)
# Tools ki list
tools = [search]

print("Tools ready!")
print(f"Tool ka naam: {search.name}")  
print(f"Tool kya karta hai: {search.description}")

# Agent banao
agent = create_react_agent(
    model=llm,
    tools=tools,
)

print("Agent ready!")

# Agent ko kaam do
result = agent.invoke({
    "messages": [
        {"role": "user", "content": "What is the latest news about AI in 2026?"}
    ]
})

# Result print karo
print("\nAgent ka jawab:")
print(result["messages"][-1].content)

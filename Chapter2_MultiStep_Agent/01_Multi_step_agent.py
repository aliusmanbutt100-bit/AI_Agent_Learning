#In multistep the agent solve the given query in multiple steps as u can see this in its output so the code is same but we do this to see that agent solve simple question in 1 sstep but for complex question agent solves it in multiple steps
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
from langchain_core.tools import tool
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatOpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    model="dots-studio/dots-3-note-preview:free"
)

# Tool 1 — Web Search
search = TavilySearch(
    api_key=os.getenv("TAVILY_API_KEY"),
    max_results=3
)

# Tool 2 — Calculator
@tool
def calculator(expression: str) -> str:
    """
    Calculate mathematical expressions.
    Use this for any math calculation.
    Input should be a math expression like '100/5' or '25*48'.
    """
    try:
        result = eval(expression)
        return f"Result: {result}"
    except Exception as e:
        return f"Error: {str(e)}"

tools = [search, calculator]

agent = create_react_agent(
    model=llm,
    tools=tools
)

# Multi-step task do
result = agent.invoke({
    "messages": [
        {
            "role": "user",
            "content": "Find Pakistan's exact 2023 census population and land area in km². Calculate density."
        }
    ]
})

print("Agent ka jawab:")
print(result["messages"][-1].content)

# now see each step of agent
print("\n--- All steps of Agent ---")
for message in result["messages"]:
    print(f"\nType: {type(message).__name__}")
    print(f"Content: {message.content[:200]}")

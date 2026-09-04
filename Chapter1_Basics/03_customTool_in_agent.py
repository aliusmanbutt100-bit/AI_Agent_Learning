#here we will use our custom tool in agent
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

# LLM
llm = ChatOpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    model="dots-studio/dots-3-note-preview:free")

# Custom calculator tool
@tool
def calculator(expression: str) -> str:
    """
    Calculate mathematical expressions.
    Use this when user asks any math calculation.
    Input should be a math expression like '25*48' or '100/4+10'.
    """
    try:
        result = eval(expression)
        return f"Answer: {result}"
    except Exception as e:
        return f"Error: {str(e)}"

tools = [calculator]

# Agent banao
agent = create_react_agent(
    model=llm,
    tools=tools
)

# Agent ko math sawaal do
result = agent.invoke({
    "messages": [
        {"role": "user", "content": "What is 4 multiplied by 8?"}
    ]
})

print("Agent ka jawab:")
print(result["messages"][-1].content)
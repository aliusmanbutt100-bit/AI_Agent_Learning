#i try user input myself in agent with memory
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
while True:
    msg=input("enter the msg:")
    
    result1 = agent.invoke({
          "messages": [{"role": "user", "content": msg}]
    }, config=config)  # ← config pass kiya
      
    print(result1["messages"][-1].content)
    if msg == "exit".lower():
        break
 
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
def get_product_info(product_name: str) -> str:
    """Get Styluxe Wears product information. Input should be product name."""
    products = {
        "white t-shirt": "Price: 2000 PKR, Cotton 100%, Available",
        "printed t-shirt": "Price: 2500 PKR, Cotton 100%, Available",
        "black t-shirt": "Price: 2000 PKR, Cotton 100%, Available",
    }
    for key in products:
        if key in product_name.lower():
            return products[key]
    return "Product not found"

@tool
def calculator(expression: str) -> str:
    """Calculate math. Input should be like '25*48'."""
    try:
        return f"Result: {eval(expression)}"
    except:
        return "Invalid expression"

tools = [get_product_info, calculator]
memory = MemorySaver()

# System prompt — agent ki personality
system_prompt = """You are a customer service agent for Styluxe Wears — 
a premium Pakistani clothing brand.

Your rules:
- Only answer about Styluxe Wears products and policies
- Be polite and friendly
- If asked anything unrelated say: 'I can only help with Styluxe Wears queries!'
- Always end with: 'Thank you for choosing Styluxe Wears! 👕'
"""

# Agent banao system prompt ke saath
agent = create_react_agent(
    model=llm,
    tools=tools,
    checkpointer=memory,
    prompt=system_prompt  # ← system prompt add kiya
)

config = {"configurable": {"thread_id": "customer_1"}}

# Test 1 — product query
result1 = agent.invoke({
    "messages": [{"role": "user", "content": "What is the price of white t-shirt?"}]
}, config=config)
print("Reply 1:", result1["messages"][-1].content)

# Test 2 — unrelated query
result2 = agent.invoke({
    "messages": [{"role": "user", "content": "What is the weather today?"}]
}, config=config)
print("\nReply 2:", result2["messages"][-1].content)
#now here we r going to add both custom tools(calculator,data return) in our agent
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
#custom data return tool
@tool
def get_product_info(product_name: str) -> str:
    """
    Get information about Styluxe Wears products.
    Use this when user asks about products, prices, or availability.
    Input should be a product name like 'white t-shirt' or 'printed tshirt'.
    """
    products = {
        "white t-shirt": "Price: 2000 PKR, Material: 100% cotton, Available: Yes",
        "printed t-shirt": "Price: 2500 PKR, Material: 100% cotton, Available: Yes",
        "black t-shirt": "Price: 2000 PKR, Material: 100% cotton, Available: Yes",
    }
    
    # Product dhundo
    for key in products:
        if key in product_name.lower():
            return products[key]
    
    return "Product not found in our catalog"
    

tools = [calculator,get_product_info]      #add both tools name here

# Agent banao
agent = create_react_agent(
    model=llm,
    tools=tools
)

# Agent ko math sawaal do
result = agent.invoke({
    "messages": [
        {"role": "user", "content": "What is the price of white t-shirt and also calculate 2000 * 3?"}
    ]
})

print("Agent reply:")
print(result["messages"][-1].content)

#now agent is answering for both tools together
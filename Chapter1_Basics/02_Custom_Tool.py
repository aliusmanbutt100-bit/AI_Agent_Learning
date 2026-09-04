"""
Previously we use a ready_made tool like tavily but now here we learn how to make tool based on our need such as file reader tool,calculator tool,database tool etc
Syntax:
from langchain_core.tools import tool
@tool   #decorator
def tool_name(input:str) -> str:
    Here u write the description like wht this tool can do and agent will read your description(write it as a comment)
    return "result"
"""
from langchain_core.tools import tool
@tool
def calculator(expression:str) -> str:
    """
    calculate the mathematial expression.
    use this when user ask any math calculation
    input should be a math expression like '25*48' or'100/4+10'
    """
    try:
        result=eval(expression)
        return f"Answer:{result}"
    except Exception as e:
        return f"Error:{str(e)}"
    
# Tool test karo — agent ke bina
print(calculator.name)
print(calculator.description)
print(calculator.invoke("25 * 48"))
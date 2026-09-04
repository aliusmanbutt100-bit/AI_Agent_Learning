#Here is some built in function in langraph that we r going to use in next project of building agent with langraph
# from langgraph.prebuilt import ToolNode          # ready-made node jo tool khud chala deta hai
# from langgraph.graph.message import add_messages  # messages list ko auto-append karta hai
# from langchain_core.tools import tool             # custom tool banane ke liye decorator
# from typing import Annotated                       # extra metadata (add_messages) type ke sath jodne ke liye

# llm_with_tools = llm.bind_tools([calculator])       # LLM ko tools ke baare mein batata hai

# response.tool_calls                                 # check: LLM ne tool maanga ya nahi (khali/na-khali)

# tool_node = ToolNode([calculator])                   # tool ko run karne wala node

# class AgentState(TypedDict):
#     messages: Annotated[list, add_messages]          # messages list, naye messages auto add hote hain
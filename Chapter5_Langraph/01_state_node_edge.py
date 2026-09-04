#Pahly ham use karty thy create agent but ab ham khud sy bannaty hai pura workflow or ham decide karty hai agent kaisy kam kary ga
"""
Part 1:
State is like a box on which function is performed and it has all the field that we use in nodes
Syntax:
from typing import TypedDict

class StateName(TypedDict):
    field1: type
    field2: type
    field3: type    flied jo chahye or unki type ka name likhna hai
Example:
class ChatState(TypedDict):
    user_message: str
    bot_response: str
    history: list
Part 2:
Node is a simple python function.it basically takes state do some work on it and return the updated state
Syntax:
def function_name(state: StateName) -> dict:
    # yahan kaam karo
    return {"jo_key_update_hui": "uski_nayi_value"}
Part 3:
Edge means connected the nodes in the sequence u want and we do it in following steps:
1-Make a graph object
graph=stateGraph(NewsState)   stategraph ik class hai and jo langraph.graph sy import hoti hai and newstate jo hamne state ka nam rakha tha
2-Adding nodes(we register the function in graph that we made)
graph.add_node("any_name/search",search_node)
graph.add_node("any_name/summarize",summarize_node)
3-Add Edges
graph.add_edge("search", "summarize") it means summarize will work after summarize node finish its work
But we also need to tell from where the graph will start
from langgraph.graph import StateGraph, START, END

graph.add_edge(START, "search")
graph.add_edge("summarize", END)

"""

# #State
# from typing import TypedDict
# class NewsState(TypedDict):
#     topic: str
#     search_results: str
#     summary: str
# #Node 1
# def search_node(state: NewsState) -> dict:
#     topic = state["topic"]              # state se topic nikala
#     result = search_tool.invoke(topic)  # us topic se search kiya
#     return {"search_results": result}   # naya data return kiya
# #Node 2
# def summarize_node(state: NewsState) -> dict:
#     search_results = state["search_results"]                  # state se search ka result nikala
#     result = llm.invoke(f"Summarize this: {search_results}")   # LLM ko clear instruction ke saath data diya
#     return {"summary": result}                                 # summary key mein result return kiya
# #Add Edges
# graph=stateGraph(NewsState)
# graph.add_node("search",search_node)
# graph.add_node("summarize",summarize_node)
# graph.add_edge("search", "summarize")
# from langgraph.graph import StateGraph, START, END

# graph.add_edge(START, "search")
# graph.add_edge("summarize", END)

# app=graph.compile() now it is able to run

    

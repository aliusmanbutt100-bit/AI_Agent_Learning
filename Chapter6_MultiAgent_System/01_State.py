#STATE:
"""
In multiagent the state is bit change to carry more information

class MultiAgentState(TypedDict):
    messages: Annotated[list, add_messages]  ->in message all agents add their work in it
    next_agent: str                          ->supervisor agent set this node to tell which agent will use next 

"""

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
from typing import TypedDict, Annotated
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatOpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    model="dots-studio/dots-3-note-preview:free"
)

search_tool = TavilySearch(api_key=os.getenv("TAVILY_API_KEY"), max_results=3)


# STATE
# messages -> poora conversation/data (research, written content, sab yahan add hota hai)
# next_agent -> Supervisor yahan decide karta hai ab kis agent ki baari hai
class MultiAgentState(TypedDict):
    messages: Annotated[list, add_messages]
    next_agent: str


# SUPERVISOR NODE
# Ye "manager" hai - state (ab tak ka conversation) dekh ke LLM se puchta hai
# ke ab kaam kis agent ko dena hai. Jawab next_agent field mein save karta hai.
def supervisor_node(state: MultiAgentState) -> dict:
    prompt = f"""Ye conversation dekho: {state['messages']}
    Batao agla kaam kis agent ko dena hai: 'researcher', 'writer', ya 'done' agar sab complete ho gaya.
    Sirf ek word return karo."""

    decision = llm.invoke(prompt)
    return {"next_agent": decision.content.strip()}


# RESEARCHER NODE
# Sirf research/search karta hai. Result ko messages list mein "add" karta hai
# (overwrite nahi karta) taake Supervisor baad mein poora data dekh sake.
def researcher_node(state: MultiAgentState) -> dict:
    last_message = state["messages"][-1]
    result = search_tool.invoke(last_message.content)
    return {"messages": [f"Research findings: {result}"]}


# WRITER NODE
# Ab tak ke messages (jisme research data bhi hai) dekh ke content likhta hai.
def writer_node(state: MultiAgentState) -> dict:
    context = state["messages"]
    result = llm.invoke(f"Write content based on this research: {context}")
    return {"messages": [result.content]}


# ROUTING FUNCTION
# Ye conditional edge ka "decision maker" hai. Supervisor node ne already
# next_agent field mein decision save kar diya tha - ye function bas
# wahi value nikal ke return karta hai, taake graph pata kare agla node kaunsa chalega.
def route_next(state: MultiAgentState) -> str:
    return state["next_agent"]


# GRAPH BANANA
graph = StateGraph(MultiAgentState)

# Teeno nodes register kiye
graph.add_node("supervisor", supervisor_node)
graph.add_node("researcher", researcher_node)
graph.add_node("writer", writer_node)

# Graph hamesha supervisor se shuru hoga
graph.add_edge(START, "supervisor")

# Conditional edge: supervisor ke decision (route_next) ke hisaab se
# agla node choose hota hai - researcher, writer, ya khatam (END)
graph.add_conditional_edges(
    "supervisor",
    route_next,
    {
        "researcher": "researcher",
        "writer": "writer",
        "done": END
    }
)

# Researcher ya Writer apna kaam khatam karne ke baad WAPIS supervisor
# ke paas jate hain, taake supervisor agla decision le sake
graph.add_edge("researcher", "supervisor")
graph.add_edge("writer", "supervisor")

# Graph ko runnable banaya
app = graph.compile()


# RUN
result = app.invoke({
    "messages": [("user", "Write a short post about latest AI news")],
    "next_agent": ""
})

# Final message (writer ka output) print karo
print(result["messages"][-1].content)
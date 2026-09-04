#ye ik workflow tha ky jaab agent ko summarize karny ka bola jai toh wo pahly ye kary then ye this is what langraph is
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
from typing import TypedDict
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatOpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    model="dots-studio/dots-3-note-preview:free"
)

search_tool = TavilySearch(
    api_key=os.getenv("TAVILY_API_KEY"),
    max_results=3
)

class NewsState(TypedDict):
    topic: str
    search_results: str
    summary: str

def search_node(state: NewsState) -> dict:
    topic = state["topic"]
    result = search_tool.invoke(topic)
    return {"search_results": result}

def summarize_node(state: NewsState) -> dict:
    search_results = state["search_results"]
    result = llm.invoke(f"Summarize this: {search_results}")
    return {"summary": result}

# Graph banaya
graph = StateGraph(NewsState)

# Nodes add kiye
graph.add_node("search", search_node)
graph.add_node("summarize", summarize_node)

# Edges add kiye (flow define kiya)
graph.add_edge("search", "summarize")
graph.add_edge(START, "search")
graph.add_edge("summarize", END)

# Graph compile kiya — ab ye run karne layak hai
app = graph.compile()

# Graph run kiya
final_state = app.invoke({"topic": "what is AI news today"})
print(final_state["summary"].content) #i skip .content and it gives meta data also like tokens and id so thats why use .content bcz it give u clean content
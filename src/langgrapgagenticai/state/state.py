from typing import Annotated
from typing_extensions import TypedDict, List
from langgraph.graph.message import add_messages

class State(TypedDict):
    """
    The class that represents the structure 
    of the State of the graph
    """
    messages: Annotated[List,add_messages]
    news_data: list
    summary:str
    filename:str
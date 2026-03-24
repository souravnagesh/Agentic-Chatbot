from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import tools_condition
from src.langgrapgagenticai.tools.search_tool import get_tools, create_tool_node
from src.langgrapgagenticai.state.state import State
from src.langgrapgagenticai.nodes.basic_chatbot_node import BasicChatbotNode
from src.langgrapgagenticai.nodes.chatbot_with_tool_node import ChatbotWithToolNode

class GraphBuilder:
    def __init__(self, model):
        self.llm= model
        self.graphbuilder= StateGraph(State)
    
    def basic_chatbot_build_graph(self):
        """
        Builds a basic chatbot graph using Langgraph.
        This method initializes a chatbot node using the `BasicChatBot` class
        and integrate it into the graph. The chatbot node is set as both the 
        entry and exit  point of the graph.
        """

        self.basic_chatbot_node= BasicChatbotNode(self.llm)

        self.graphbuilder.add_node("chatbot",self.basic_chatbot_node.process)
        self.graphbuilder.add_edge(START, "chatbot")
        self.graphbuilder.add_edge("chatbot",END)
    
    def chatbot_with_tool_build_graph(self):
        """
        Builds an advanced chatbot graph with tool integration.
        This method creates a chatbot graph includes both a chatbot node
        and a tool node. It defines tools, initialize the chatbot with tool
        capabilities, and sets up conditional and direct edges between nodes.
        The chatbot node is set as the entry point

        """
        tools= get_tools()
        tool_node= create_tool_node(tools)

        llm= self.llm

        obj_chatbot_node= ChatbotWithToolNode(llm)
        chatbot_node=obj_chatbot_node.create_chatbot(tools)

        self.graphbuilder.add_node("chatbot",chatbot_node)
        self.graphbuilder.add_node("tools", tool_node)

        self.graphbuilder.add_edge(START, "chatbot")
        self.graphbuilder.add_conditional_edges("chatbot", tools_condition)
        self.graphbuilder.add_edge("tools", "chatbot")
    
    def setup_graph(self, usecase:str):
        if usecase =="Basic Chatbot":
            self.basic_chatbot_build_graph()
        
        if usecase =="Chatbot with Web":
            self.chatbot_with_tool_build_graph()

        return self.graphbuilder.compile()
        

from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import tools_condition
from src.langgraph_agentic_ai.tools.search_tool import get_tools, create_tool_node
from src.langgraph_agentic_ai.state.state import State
from src.langgraph_agentic_ai.nodes.basic_chatbot_node import BasicChatbotNode
from src.langgraph_agentic_ai.nodes.chatbot_with_tool_node import ChatbotWithToolNode
from src.langgraph_agentic_ai.nodes.ai_news_node import AINewsNode

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

    def ai_news_builder_grpah(self):

        ai_news_node= AINewsNode(self.llm)

        self.graphbuilder.add_node("fetch_news",ai_news_node.fetch_news)
        self.graphbuilder.add_node("summarize_news",ai_news_node.summarize_news)
        self.graphbuilder.add_node("save_results",ai_news_node.save_result)

        self.graphbuilder.add_edge(START,"fetch_news")
        self.graphbuilder.add_edge("fetch_news","summarize_news")
        self.graphbuilder.add_edge("summarize_news","save_results")
        self.graphbuilder.add_edge("save_results",END)

    
    def setup_graph(self, usecase:str):
        if usecase =="Basic Chatbot":
            self.basic_chatbot_build_graph()
        
        if usecase =="Chatbot with Web":
            self.chatbot_with_tool_build_graph()
        
        if usecase =="AI News":
            self.ai_news_builder_grpah()

        return self.graphbuilder.compile()
        

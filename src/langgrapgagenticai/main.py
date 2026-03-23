import streamlit as st
from src.langgrapgagenticai.ui.streamlitui.loadui import LoadStreamlitUI
from src.langgrapgagenticai.LLMs.openaillm import OpenAILLM 
from src.langgrapgagenticai.graph.graph_builder import GraphBuilder
from src.langgrapgagenticai.ui.streamlitui.display_results import DisplayResultsStreamlit

def load_langgraph_agenticai_app():
    """
    Loads and runs the langgraph Agentic AI application with Streamlit UI.
    This functions initializes the UI, handles user input, configure the LLM model,
    set up the graph based on the selected usecase and display the output while implementing
    exception handling  for robustness

    """
    ## Load UI
    ui= LoadStreamlitUI()
    user_input= ui.load_streamlit_ui()

    if not user_input:
        st.error("Error, Failed to load the user input from UI")
        return
    
    user_message= st.chat_input("Enter your message:")

    if user_message:
        try:
            config_llm= OpenAILLM(user_control_input=user_input)
            model= config_llm.get_llm_model()

            if not model:
                st.error("Error: LLM model could not be initialized")
                return
            
            ## Initialize and setup graph based on usecases
            usecase= user_input.get("selected_usecase")
            if not usecase:
                st.error("Error: No usecase selected")
                return
            
            # Graph Builder
            graph_builder= GraphBuilder(model)
            try:
                graph= graph_builder.setup_graph(usecase)
                DisplayResultsStreamlit(usecase,graph,user_message).display_results_on_ui()
            except Exception as e:
                st.error(f"Error: Graph set up failed {e}")
                return
            

        except Exception as e:
            st.error(f"Encounter an unexpected error: {e}")
            return
    
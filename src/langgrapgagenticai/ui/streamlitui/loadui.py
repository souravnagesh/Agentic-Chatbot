import os
import streamlit as st
from src.langgrapgagenticai.ui.uiconfigfile import Config

class LoadStreamlitUI:
    def __init__(self):
        self.config=Config()
        self.user_controls={}
    
    def load_streamlit_ui(self):
        st.set_page_config(page_title="🤖 "+ self.config.get_page_title(), layout="wide")
        st.header("🤖 "+ self.config.get_page_title())

        with st.sidebar:
            # Get option from Config
            llm_options= self.config.get_llm_options()
            usecase_options= self.config.get_usecase_options()
            
            # LLM Selection
            self.user_controls["selected_llms"] = st.selectbox("Select LLM", llm_options)
            # Model Selection
            if self.user_controls["selected_llms"] == "Openai":
                model_options= self.config.get_openai_usecase_options()
                self.user_controls["selected_openai_model"] = st.selectbox("Select Model", model_options)
                self.user_controls["OPENAI_API_KEY"]= st.session_state["OPENAI_API_KEY"]= st.text_input("API KEY", type="password")
                # Validate API key
                if not self.user_controls["OPENAI_API_KEY"]:
                    st.warning("Please enter you OpenAI API key to proceed further")
            # Usecase Selection
            self.user_controls["selected_usecase"]=st.selectbox("Select Usecases", usecase_options)
        
        return self.user_controls

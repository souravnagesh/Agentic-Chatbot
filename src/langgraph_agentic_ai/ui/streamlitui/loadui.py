import os
import streamlit as st
from src.langgraph_agentic_ai.ui.uiconfigfile import Config

class LoadStreamlitUI:
    def __init__(self):
        self.config=Config()
        self.user_controls={}
    
    def load_streamlit_ui(self):
        st.set_page_config(page_title="🤖 "+ self.config.get_page_title(), layout="wide")
        st.header("🤖 "+ self.config.get_page_title())
        st.session_state.timeframe=''
        st.session_state.IsFetchButtonClicked= False

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

            if self.user_controls["selected_usecase"]=="Chatbot with Web" or self.user_controls["selected_usecase"]== "AI News":
                os.environ["TAVILY_API_KEY"]=self.user_controls["TAVILY_API_KEY"] =st.session_state["TAVILY_API_KEY"]= st.text_input("TAVILY API KEY", type="password")
                
                if not self.user_controls["TAVILY_API_KEY"]:
                    st.warning("Please enter the Tavily API key to proceed further")
            
            if self.user_controls["selected_usecase"]=="AI News":
                st.subheader("AI News explorer")

                with st.sidebar:
                    time_frame= st.selectbox(
                        "Select Time Frame",
                        ["Daily", "Weekly", "Monthly"],
                        index=0
                    )
                if st.button("Fetch Latest AI News", use_container_width=True):
                    st.session_state.IsFetchButtonClicked= True
                    st.session_state.timeframe= time_frame
        
        return self.user_controls

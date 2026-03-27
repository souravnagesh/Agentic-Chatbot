import os
import streamlit as st
from langchain_openai import ChatOpenAI

class OpenAILLM:
    def __init__(self, user_control_input):
        self.user_control_input= user_control_input
    
    def get_llm_model(self):
        try:
            openai_api_key= self.user_control_input["OPENAI_API_KEY"]
            selected_openai_model= self.user_control_input["selected_openai_model"]

            if openai_api_key=="" and os.environ["OPENAI_API_KEY"]=="":
                st.error("Please Enter the OpenAI API key")
         
            llm= ChatOpenAI(api_key=openai_api_key, model=selected_openai_model)
        except Exception as e:
            raise ValueError(f"Error occured with Exception {e}")
        return llm
        


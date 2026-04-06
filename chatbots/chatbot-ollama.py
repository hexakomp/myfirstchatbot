from dotenv import load_dotenv
import os
from langchain_ollama import ChatOllama
import gradio as gr


# Initialize the language model
llm = ChatOllama(
    url="http://localhost:11434",
    model="gemma3:270m",
    temperature=0.7,
    api_key="ollama"
)

# Define the messages for the chatbot

systemmessage= "You are a Teacher , answer the question in a concise manner."

def chatbot_response(user_input):
    messages = [
        ("system", systemmessage),
        ("human", user_input),
        
    ]
    ai_msg = llm.invoke(messages).content
    return ai_msg


# Create the Gradio interface
iface = gr.Interface(fn=chatbot_response, inputs="text", outputs="text", title="My First Chatbot")
# Launch the interface
iface.launch()






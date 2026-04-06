from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI
import gradio as gr

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


# Initialize the language model
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    temperature=0.7,
    api_key=GOOGLE_API_KEY
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






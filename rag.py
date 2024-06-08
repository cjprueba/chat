from crewai_tools import PDFSearchTool
from crewai_tools import TXTSearchTool

from crewai import Agent, Task
import os 


import streamlit as st
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
import uuid
import asyncio
import PyPDF2
import docx
import json
import os
import datetime


# Initialize the tool allowing for any PDF content search if the path is provided during execution


#tool = PDFSearchTool()


# Initialize the tool with a specific PDF path for exclusive search within that document
#tool = PDFSearchTool(pdf='C:/users/cjunn/Downloads/CONTRATO DE TRABAJO #1.pdf')
tool = TXTSearchTool(txt='D:/PA/REPOSITORIOS/PERSONALES/RAG-CREWAI/toku.txt')



print("PASE POR AQUI DE VUELTA")

assistant = Agent(
role='Assistant',
goal='You perfectly know how to assist any customer using the provided txt file and searching info via RAG tool',
backstory=("You are an expert assistant. Response always in Spanish or Portuguese depending on the user's language. Do not make up any response, just use the information in the txt file."
    f"La fecha y hora actual es: {str(datetime.datetime.now())}"
    ),
verbose=True,
allow_delegation=False,
tools=[tool]
)




async def get_response_from_bedrock(pregunta, tool, assistant):
    try:

        test_task = Task(
          description=pregunta,
          tools=[tool],
          agent=assistant,
          expected_output='Response all the questions in Spanish'
        )

        
        return test_task.execute()

    except Exception as e:
        return f"Error: {e}"

# Streamlit app
st.title("Asistente Toku Toku")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        response_placeholder = st.empty()

        try:
            response_json = json.loads(message["content"])
            response_placeholder.json(response_json)
        except json.JSONDecodeError as e:
            response_placeholder.markdown(message["content"])
            
@st.experimental_fragment
def interfaz(tool, assistant):
    
    with st.spinner("waiting"):
        # Fetch and stream the assistant's response
        response = asyncio.run(get_response_from_bedrock(prompt, tool, assistant))

    # Display the full response at once
    try:
        response_json = json.loads(response)
        response_placeholder.json(response_json)
    except json.JSONDecodeError as e:
        response_placeholder.markdown(response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

    # File uploader to let user upload a file
    # uploaded_file = st.file_uploader("Upload a file for the AI assistant to read", type=["txt", "pdf", "docx"])
    #container = st.container()

    #st.session_state.uploaded_file = None


# Accept user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Create a placeholder for the assistant's response
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        interfaz(tool, assistant)


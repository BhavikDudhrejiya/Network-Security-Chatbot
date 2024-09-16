import streamlit as st
import pandas as pd
from utils import *
from syslog_generator import generate_logs_file
from logs_engine import *

st.sidebar.image("./dataslush-logo.png", width=250)
st.sidebar.divider()
st.sidebar.title("Chat Application".upper())
section = st.sidebar.radio("Please select the section:", ["Upload Guidelines", "Use ChatBot"], horizontal=False)

if section=="Upload Guidelines":

    st.header("Upload latest firewall guidelines:".upper())

    st.divider()

    upload_pdf = st.file_uploader("Please upload PDF file:", type="pdf")

    if st.button("Upload"):
        project_path = os.getcwd()
        folder_name = "assets"
        create_folder_if_not_exists(folder_path=project_path+"/"+folder_name)
        pdf_file_path = os.path.join(project_path, folder_name, upload_pdf.name)
        save_pdf(upload_pdf, pdf_file_path)
        st.success(f"PDF file {upload_pdf.name} has been uploaded successfully...")
        embeddings_folder_name = "embeddings"
        create_folder_if_not_exists(folder_path=project_path+"/"+embeddings_folder_name)
        ChatEngine().load_pdf_and_generate_embeddings(document_path=pdf_file_path)
        st.success(f"Embeddings for PDF file {upload_pdf.name} has been generated successfully...")
else:
    on = st.toggle("CISCO ASA Logs")

    st.session_state.chat1 = initialize_chat()
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    st.session_state.chat2 = initialize_logs()
    if "logs_history" not in st.session_state:
        st.session_state.logs_history = []

    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_prompt = st.chat_input("Ask anything about CISCO firewall...")

    if user_prompt:
        st.chat_message("user").markdown(user_prompt)
        st.session_state.chat_history.append({"role": "user", "content": user_prompt})
        if on:
            generate_logs_file(log_count=12, add_label="Yes", gen_seen="yes", filename="./syslogs/logs.csv")
            logs = pd.read_csv(filepath_or_buffer="./syslogs/logs.csv", on_bad_lines='skip').to_json()

            response = st.session_state.chat2.ask_logs(query=user_prompt, logs=logs)
        else:
            response = st.session_state.chat1.ask_pdf(query=user_prompt)

            if not response:
                response = "Unable to generate response."

        with st.chat_message("assistant"):
            st.markdown(response)
        st.session_state.chat_history.append({"role":"assistant", "content":response})

    if st.sidebar.button("Reset Chat", use_container_width=True, type='primary', help="Double click here to clear the chat."):
        st.session_state.chat_history = []
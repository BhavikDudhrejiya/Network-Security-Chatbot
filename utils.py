import os
import streamlit as st
from chat_engine import *
from logs_engine import *

def save_pdf(file, save_path):
    with open(save_path, "wb") as f:
        f.write(file.getbuffer())

def create_folder_if_not_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Folder '{folder_path}' created successfully.")
    else:
        print(f"Folder '{folder_path}' already exists.")

@st.cache_resource
def initialize_chat():
    chat = ChatEngine()
    return chat

@st.cache_resource
def initialize_logs():
    logs_chat = LogsChatEngine()
    return logs_chat
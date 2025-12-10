import streamlit as st
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings, ChatOllama
from config import PASTA_MEMORIA, MODELO_LLM, TEMPERATURA
import os

@st.cache_resource
def get_llm():
    return ChatOllama(model=MODELO_LLM, temperature=TEMPERATURA)

@st.cache_resource
def get_embedding_function():
    return OllamaEmbeddings(model="all-minilm")

def carregar_banco(nome_caso):
    caminho = os.path.join(PASTA_MEMORIA, nome_caso)
    if not os.path.exists(caminho): os.makedirs(caminho)
    
    # Previne erro de lock do Windows fechando conexão anterior
    if "vectorstore" in st.session_state and st.session_state.vectorstore:
        try: st.session_state.vectorstore._client._system.stop()
        except: pass
        
    return Chroma(
        collection_name=nome_caso,
        embedding_function=get_embedding_function(),
        persist_directory=caminho
    )
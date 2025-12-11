import streamlit as st
import whisper

@st.cache_resource
def get_whisper_model():
    
    # Modelo base CPU

    return whisper.load_model("base")

def transcrever_audio(caminho_audio):
    model = get_whisper_model()
    try:
        result = model.transcribe(caminho_audio)
        return result["text"]
    except Exception as e: 
        return f"Erro na transcrição de áudio: {e}. Verifique se o FFmpeg está instalado."
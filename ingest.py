import streamlit as st
import tempfile
import os
import time
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from ocr import ler_imagem, ler_pdf, ler_planilha
from audio import transcrever_audio

def processar_arquivos(vectorstore, arquivos):
    if not arquivos: return 0, ""
    docs_acumulados = []
    texto_sessao = ""
    progresso = st.progress(0, text="Processando arquivos...")
    
    for i, arquivo in enumerate(arquivos):
        ext = arquivo.name.split('.')[-1].lower()
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{ext}") as tmp:
            tmp.write(arquivo.getvalue())
            tmp_path = tmp.name
        
        texto_extraido = ""
        origem = ""
        
        try:
            if ext in ['jpg', 'jpeg', 'png']:
                origem = "IMAGEM"
                texto_extraido = ler_imagem(tmp_path)
            elif ext == 'pdf':
                origem = "PDF"
                texto_extraido = ler_pdf(tmp_path)
            elif ext in ['wav', 'mp3']:
                origem = "ÁUDIO"
                texto_extraido = transcrever_audio(tmp_path)
            elif ext in ['xlsx', 'xls', 'csv']:
                origem = "PLANILHA"
                texto_extraido = ler_planilha(tmp_path)

            if texto_extraido and len(texto_extraido.strip()) > 2:
                doc_final = f"--- {origem}: {arquivo.name} ---\n{texto_extraido}\n"
                docs_acumulados.append(Document(page_content=doc_final, metadata={"source_name": arquivo.name}))
                texto_sessao += doc_final + "\n\n"
            else:
                st.toast(f"⚠️ {arquivo.name} parece vazio.")

        except Exception as e:
            st.error(f"Erro em {arquivo.name}: {e}")
        finally:
            if os.path.exists(tmp_path): os.remove(tmp_path)
        progresso.progress((i + 1) / len(arquivos))
        
    if docs_acumulados and vectorstore:
        splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
        chunks = splitter.split_documents(docs_acumulados)
        
        # Batch fix para ChromaDB
        
        BATCH_SIZE = 4000
        for i in range(0, len(chunks), BATCH_SIZE):
            vectorstore.add_documents(chunks[i:i+BATCH_SIZE])
            time.sleep(0.1)
    
    progresso.empty()
    return len(docs_acumulados), texto_sessao
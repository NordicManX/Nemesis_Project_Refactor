import streamlit as st
import time
import re
import gc
import shutil
import os

# Importando os módulos
from config import get_tesseract_cmd, PASTA_MEMORIA
from utils import carregar_config_json, salvar_config_json, faxina_inicial, gerar_word, listar_casos_visiveis
from store import carregar_banco
from ingest import processar_arquivos
from prompt import fluxo_de_resposta

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="NEMESIS AI PROJECT", page_icon="🧬", layout="wide")

# Inicialização de Estado
if "vectorstore" not in st.session_state: st.session_state.vectorstore = None
if "caso_selecionado" not in st.session_state: st.session_state.caso_selecionado = None
if "memoria_imediata" not in st.session_state: st.session_state.memoria_imediata = ""
if "messages" not in st.session_state: st.session_state.messages = []
if "ultimas_fontes" not in st.session_state: st.session_state.ultimas_fontes = []

# Faxina na inicialização
faxina_inicial()

# --- CSS ---
st.markdown("""
<style>
    .stApp { background-color: #1e1e1e; color: #e0e0e0; }
    [data-testid="stSidebar"] { background-color: #121212; border-right: 1px solid #333; }
    .stButton button { text-align: left; border: none; background: transparent; color: #cfcfcf; padding: 8px 0px; width: 100%; }
    .stButton button:hover { color: #fff; padding-left: 5px; }
    [data-testid="stPopover"] > button { border: none; background: transparent; color: #a8c7fa; font-weight: bold; font-size: 1.5em; padding: 0px; width: 30px; }
    .source-box { background-color: #25262b; padding: 12px; border-radius: 8px; border-left: 3px solid #6c5ce7; margin-top: 8px; font-size: 0.85em; color: #b2bec3; }
    .raw-text { font-family: monospace; font-size: 0.8em; color: #a29bfe; background-color: #151515; padding: 10px; border-radius: 5px; max-height: 200px; overflow-y: auto; }
</style>
""", unsafe_allow_html=True)

# --- AÇÕES DE BARRA LATERAL ---
def acao_excluir(nome):
    st.session_state.vectorstore = None
    st.session_state.caso_selecionado = None
    st.session_state.memoria_imediata = ""
    st.session_state.messages = []
    gc.collect()
    cfg = carregar_config_json()
    if nome not in cfg["trash"]: cfg["trash"].append(nome)
    if nome in cfg.get("pinned", []): cfg["pinned"].remove(nome)
    salvar_config_json(cfg)
    try: shutil.rmtree(os.path.join(PASTA_MEMORIA, nome))
    except: pass
    st.toast("🗑️ Caso enviado para lixeira.")
    time.sleep(0.5)
    st.rerun()

def acao_fixar(nome):
    cfg = carregar_config_json()
    if nome in cfg["pinned"]: cfg["pinned"].remove(nome)
    else: cfg["pinned"].append(nome)
    salvar_config_json(cfg)
    st.rerun()

def acao_renomear(antigo, novo):
    if not novo: return
    novo_limpo = re.sub(r'[^a-zA-Z0-9_-]', '', novo.strip().replace(" ", "_")).strip("_-")
    if not novo_limpo: return
    st.session_state.vectorstore = None
    gc.collect()
    try:
        os.rename(os.path.join(PASTA_MEMORIA, antigo), os.path.join(PASTA_MEMORIA, novo_limpo))
        cfg = carregar_config_json()
        if antigo in cfg["pinned"]:
            cfg["pinned"].remove(antigo)
            cfg["pinned"].append(novo_limpo)
        salvar_config(cfg)
        st.session_state.caso_selecionado = novo_limpo
        st.toast("✅ Renomeado!")
        st.rerun()
    except: st.error("⚠️ Erro ao renomear.")

# --- APP ---
def main():
    with st.sidebar:
        st.header("🗂️ Histórico")
        if st.button("➕ Novo Caso", use_container_width=True):
            st.session_state.caso_selecionado = None
            st.session_state.memoria_imediata = ""
            st.session_state.messages = []
            st.rerun()
        st.markdown("---")
        
        casos = listar_casos_visiveis()
        cfg = carregar_config_json()
        
        for caso in casos:
            c1, c2 = st.columns([0.85, 0.15])
            with c1:
                icone = "📌" if caso in cfg["pinned"] else "📁"
                if st.button(f"{icone} {caso}", key=f"btn_{caso}", use_container_width=True):
                    st.session_state.caso_selecionado = caso
                    st.session_state.memoria_imediata = ""
                    st.session_state.messages = []
                    st.session_state.vectorstore = None
                    st.rerun()
            with c2:
                with st.popover("⋮"):
                    st.caption(f"Caso: {caso}")
                    if st.button(f"📌 Fixar", key=f"p_{caso}"): acao_fixar(caso)
                    nn = st.text_input("Renomear:", value=caso, key=f"i_{caso}")
                    if st.button("✏️ Salvar", key=f"r_{caso}"): acao_renomear(caso, nn)
                    st.divider()
                    if st.button("🗑️ Excluir", key=f"d_{caso}", type="primary"): acao_excluir(caso)

        if not get_tesseract_cmd(): st.error("🚨 Tesseract não encontrado")

        # --- RODAPÉ PERSONALIZADO (AQUI ESTÁ A MUDANÇA) ---
        st.markdown("---")
        st.markdown(
            """
            <div style='text-align: center; color: #666; font-size: 0.8em; margin-top: 20px;'>
                <p>Feito por <b>NordicManX</b> ❄️⚔️</p>
                <p>🛡️ <b>Nemesis Team</b></p>
                <p>🌊 Guaratuba - Paraná</p>
                <p style='font-size: 0.7em; opacity: 0.5;'>v18.1 Stable Build</p>
            </div>
            """, 
            unsafe_allow_html=True
        )

    if st.session_state.get("caso_selecionado"):
        st.title(f"🧬 {st.session_state.caso_selecionado}")
        if not st.session_state.vectorstore:
            st.session_state.vectorstore = carregar_banco(st.session_state.caso_selecionado)
            
        # DEBUG
        if st.session_state.get("memoria_imediata"):
            with st.expander("👁️ Ver Dados Brutos"): 
                st.markdown(f"<div class='raw-text'>{st.session_state.memoria_imediata[:2000]}</div>", unsafe_allow_html=True)

        # UPLOAD
        with st.expander("📎 Anexar", expanded=False):
            files = st.file_uploader("Upload", type=["pdf", "jpg", "png", "xlsx", "csv", "wav"], accept_multiple_files=True)
            if st.button("Processar") and files:
                qtd, txt = processar_arquivos(st.session_state.vectorstore, files)
                st.session_state.memoria_imediata = txt
                st.rerun()

        # CHAT
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
                if msg["role"] == "assistant":
                    doc = gerar_word(msg["content"])
                    st.download_button("📄 Word", doc, f"Nemesis_{int(time.time())}.docx", key=f"dw_{msg['content'][:5]}")
                if msg.get("fontes"):
                    with st.expander("🔍 Fontes"):
                        for d in msg["fontes"]: st.markdown(f"<div class='source-box'>📄 {d.metadata.get('source_name')}</div>", unsafe_allow_html=True)

        if prompt := st.chat_input("Pergunte..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"): st.markdown(prompt)
            with st.chat_message("assistant"):
                resp = st.write_stream(fluxo_de_resposta(st.session_state.vectorstore, prompt))
                ft = st.session_state.get("ultimas_fontes", [])
                st.session_state.messages.append({"role": "assistant", "content": resp, "fontes": ft})
                st.rerun()
    else:
        st.markdown("# 👋 Bem-vindo ao Nemesis")
        novo = st.text_input("Novo Caso")
        if novo:
            safe = re.sub(r'[^a-zA-Z0-9_-]', '', novo.strip().replace(" ", "_")).strip("_-")
            if not safe: safe="novo"
            st.session_state.caso_selecionado = safe
            st.rerun()

if __name__ == "__main__":
    main()
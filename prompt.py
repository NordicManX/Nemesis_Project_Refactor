from langchain_core.prompts import ChatPromptTemplate
from store import get_llm
import streamlit as st

def fluxo_de_resposta(vectorstore, pergunta):
    imediato = st.session_state.get("memoria_imediata", "")
    ctx_bd = ""
    historico = []
    
    if vectorstore:
        try:
            historico = vectorstore.as_retriever(search_kwargs={"k": 5}).invoke(pergunta)
            ctx_bd = "\n\n".join([d.page_content for d in historico])
        except: pass
    
    st.session_state.ultimas_fontes = historico

    if not imediato and not ctx_bd:
        yield "Sem dados. Anexe um arquivo."
        return

    # Prompt Melhorado (Sem Filtros)

    contexto_final = f"""
    VOCÊ É UM ANALISTA DE DADOS (JURÍDICO/FINANCEIRO/TÉCNICO).
    DADOS BRUTOS (OCR/PLANILHAS/ÁUDIO):
    {imediato}
    HISTÓRICO:
    {ctx_bd}
    INSTRUÇÕES:
    1. Responda com base nos dados acima.
    2. NÃO recuse analisar imagens/planilhas. O texto acima é o conteúdo delas.
    """
    
    chain = ChatPromptTemplate.from_template("Analise e responda:\n{question}") | get_llm()

    # Concatena para garantir contexto
    
    full_q = f"{contexto_final}\n\nPERGUNTA: {pergunta}"
    
    for chunk in chain.stream({"question": full_q}):
        yield chunk.content
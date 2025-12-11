# ⚖️ NEMESIS AI PROJECT (Modular Edition)

> **Inteligência Jurídica Soberana & Multimodal**
> *Roda 100% Local. Privacidade Absoluta. Sem custos por token.*

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-red?style=for-the-badge&logo=streamlit)
![Llama 3.1](https://img.shields.io/badge/AI-Llama%203.1-orange?style=for-the-badge)
![Local](https://img.shields.io/badge/Privacy-100%25%20Local-green?style=for-the-badge)

---

## 📖 Sobre o Projeto

O **Nemesis AI** é um sistema de **RAG (Retrieval-Augmented Generation)** de última geração, desenhado para escritórios de advocacia e departamentos financeiros. Ele foi arquitetado para ingerir, processar e analisar grandes volumes de documentos complexos sem nunca enviar dados para a nuvem.

Diferente de scripts simples, esta versão utiliza uma **Arquitetura Modular**, onde cada função do sistema (visão, audição, memória, interface) opera de forma independente e organizada.

---

## 🚀 Funcionalidades Principais

### 🧠 Capacidades Cognitivas
* **Ingestão Multimodal:**
    * 📄 **PDFs:** Processamento híbrido (texto nativo + OCR para páginas digitalizadas).
    * 🖼️ **Imagens:** Leitura de documentos escaneados e fotos (JPG/PNG) com pré-tratamento de contraste.
    * 🎧 **Áudio:** Transcrição offline de alta precisão (Whisper) para áudios de audiências ou reuniões (.wav/.mp3).
    * 📊 **Planilhas:** Análise de dados financeiros em Excel (.xlsx) e CSV.
* **Correção de "Big Data":** Sistema inteligente de *Batch Processing* que fatia planilhas gigantes (+10k linhas) para evitar o travamento do banco de dados vetorial.
* **Prompt Anti-Recusa:** Engenharia de prompt avançada que impede a IA de recusar a análise de imagens ou arquivos, forçando uma resposta técnica baseada na extração de dados.

### 💻 Interface & UX
* **Painel de Controle Streamlit:** Interface moderna em *Dark Mode*.
* **Gestão de Casos (CRUD):**
    * 📌 Fixar casos prioritários.
    * ✏️ Renomear pastas de clientes.
    * 🗑️ **Soft Delete:** Sistema de lixeira segura que evita erros de travamento do Windows (`WinError 32`), ocultando o caso instantaneamente e limpando o disco na reinicialização.
* **Debug em Tempo Real:** Visualizador de dados brutos ("O que o robô leu") para auditoria.

### 📝 Saída Profissional
* **Relatórios Word:** Botão integrado para exportar qualquer resposta da IA diretamente para um arquivo `.docx` formatado.

---

## 🏗️ Arquitetura Modular

O projeto deixou de ser um arquivo único e foi refatorado para facilitar a manutenção e escalabilidade:

```text
nemesis_refactor/
│
├── app.py          # O Maestro: Gerencia a Interface (UI) e o fluxo do usuário
├── ingest.py       # O Processador: Recebe arquivos e direciona para OCR/Áudio
├── store.py        # A Memória: Gerencia o ChromaDB e Embeddings
├── ocr.py          # A Visão: Wrapper para Tesseract e PyMuPDF
├── audio.py        # A Audição: Wrapper para OpenAI Whisper
├── prompt.py       # O Cérebro: Lógica de chat e engenharia de prompt
├── config.py       # Configurações: Caminhos, constantes e detecção de ambiente
└── utils.py        # Ferramentas: JSON, Word, limpeza de arquivos
```
## 🛠️ Pré-requisitos de Sistema
Para rodar o Nemesis, seu ambiente precisa das seguintes ferramentas instaladas:

Ollama (Motor de IA):

Instale o Ollama e baixe o modelo: ollama run llama3.1

Tesseract OCR (Motor de Visão):

Instale em C:\Program Files\Tesseract-OCR.

FFmpeg (Motor de Áudio):

Necessário para o Whisper funcionar. Instale via Chocolatey (choco install ffmpeg) ou adicione ao PATH. 


### 📦 Instalação e Execução
1. Preparar o Ambiente
```
# Clone ou baixe o repositório
cd nemesis_refactor

# Crie um ambiente virtual
python -m venv venv

# Ative o ambiente
.\venv\Scripts\activate
```
### 2. Instalar Dependências
```
pip install -r requirements.txt
```

### Rodar o Sistema
```
streamlit run app.py
```

<div align="center">
  
### 🤝 Créditos e Autoria
Este projeto foi desenvolvido com foco em soberania de dados e excelência técnica.



Feito por NordicManX ❄️⚔️
🛡️ Nemesis Team 🌊 Guaratuba - Paraná

v18.1 Stable Build

</div>
   

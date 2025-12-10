# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import copy_metadata
import sys
import os
import streamlit

# --- 1. CONFIGURAÇÃO DE CAMINHOS ---
streamlit_path = os.path.dirname(streamlit.__file__)
streamlit_static = os.path.join(streamlit_path, 'static')

# --- 2. ARQUIVOS DO PROJETO ---
datas = [
    ('app.py', '.'),
    ('config.py', '.'),
    ('utils.py', '.'),
    ('store.py', '.'),
    ('audio.py', '.'),
    ('ocr.py', '.'),
    ('ingest.py', '.'),
    ('prompt.py', '.'),
    (streamlit_static, 'streamlit/static'),
]

# --- 3. METADADOS ---
packages_metadata = [
    'streamlit',
    'chromadb',
    'langchain',
    'langchain_community',
    'langchain_core',
    'langchain_ollama',
    'langchain_chroma',
    'openai-whisper',
    'pandas',
    'tqdm',
    'regex',
    'requests',
    'packaging',
    'filelock',
    'numpy',
    'pytesseract',
    'openpyxl',
    'posthog',
    'onnxruntime' # As vezes o Chroma pede isso também
]

for package in packages_metadata:
    try:
        datas += copy_metadata(package)
    except Exception:
        pass

# --- 4. IMPORTAÇÕES OCULTAS (LISTA ATUALIZADA) ---
hidden_imports = [
    # Core Streamlit
    'streamlit',
    'streamlit.runtime.scriptrunner.magic_funcs',
    'streamlit.runtime.scriptrunner.magic',
    
    # ChromaDB (A CORREÇÃO DO RUST ESTÁ AQUI)
    'chromadb',
    'chromadb.api',
    'chromadb.api.rust',            # O erro atual
    'chromadb.api.segment',         # O provável próximo erro
    'chromadb.db.impl.sqlite',      # Banco de dados físico
    'chromadb.migrations',          # Migrações de banco
    'chromadb.telemetry',
    'chromadb.telemetry.product',
    'chromadb.telemetry.product.posthog',
    'posthog',
    
    # Sklearn e Utils
    'sklearn.neighbors._typedefs', 
    'sklearn.utils._cython_blas', 
    'sklearn.neighbors._quad_tree', 
    'sklearn.tree._utils',
    
    # LangChain
    'langchain',
    'langchain_community',
    'langchain_community.document_loaders',
    'langchain_core',
    'langchain_core.prompts',
    'langchain_core.documents',
    'langchain_text_splitters',
    'langchain_chroma',
    'langchain_ollama',
    
    # Multimidia
    'whisper',
    'speech_recognition',
    'pytesseract',
    'PIL',
    'PIL.Image',
    'fitz',
    
    # Dados
    'pandas',
    'openpyxl',
    'tabulate',
    'docx', 
    'docx.document',
    'docx.oxml',
    'docx.opc.parts'
]

# --- 5. COMPILAÇÃO ---
block_cipher = None

a = Analysis(
    ['run_nemesis.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='NemesisAI',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None
)
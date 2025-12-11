import os
import sys

# DEFINIÇÃO DA PASTA RAIZ 

if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PASTA_MEMORIA = os.path.join(BASE_DIR, "banco_de_dados_nemesis")
ARQUIVO_CONFIG = os.path.join(PASTA_MEMORIA, "nemesis_config.json")

MODELO_LLM = "llama3.1"
TEMPERATURA = 0.0

# CONFIGURAÇÃO DO FFMPEG
# Adiciona a pasta bin_ffmpeg ao PATH do sistema temporariamente sendo assim, o Whisper encontra o executável sem precisar de instalação global.

caminho_ffmpeg = os.path.join(BASE_DIR, "bin_ffmpeg")
if os.path.exists(caminho_ffmpeg):
    os.environ["PATH"] += os.pathsep + caminho_ffmpeg

# CONFIGURAÇÃO DO TESSERACT 

def get_tesseract_cmd():
    # Prioridade: Pasta Local
    caminho_local = os.path.join(BASE_DIR, "bin_tesseract", "tesseract.exe")
    if os.path.exists(caminho_local):
        return caminho_local

    # Fallback: Sistema
    caminhos_sistema = [
        r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
        os.path.expanduser(r"~\AppData\Local\Tesseract-OCR\tesseract.exe")
    ]
    
    for caminho in caminhos_sistema:
        if os.path.exists(caminho):
            return caminho
            
    return None
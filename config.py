import os

# --- CAMINHOS DE SISTEMA ---
PASTA_MEMORIA = "./banco_de_dados_nemesis"
ARQUIVO_CONFIG = os.path.join(PASTA_MEMORIA, "nemesis_config.json")

# --- MODELOS ---
MODELO_LLM = "llama3.1"
TEMPERATURA = 0.0 # Zero criatividade para precisão técnica

# --- TESSERACT OCR ---
# Lista de locais onde o Tesseract costuma se esconder
CAMINHOS_TESSERACT = [
    r"C:\Program Files\Tesseract-OCR\tesseract.exe",
    r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
    os.path.expanduser(r"~\AppData\Local\Tesseract-OCR\tesseract.exe")
]

def get_tesseract_cmd():
    for caminho in CAMINHOS_TESSERACT:
        if os.path.exists(caminho):
            return caminho
    return None
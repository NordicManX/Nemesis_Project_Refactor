import pytesseract
from PIL import Image, ImageOps
import fitz  # PyMuPDF
import pandas as pd
import numpy as np
from config import get_tesseract_cmd

# Configura Tesseract na inicialização do módulo
cmd = get_tesseract_cmd()
if cmd:
    pytesseract.pytesseract.tesseract_cmd = cmd

def ler_imagem(caminho):
    if not cmd: return "ERRO: Tesseract não encontrado."
    try:
        img = Image.open(caminho)
        # Dark mode fix (inverte se for muito escuro)
        if np.mean(np.array(img.convert("L"))) < 127: 
            img = ImageOps.invert(img.convert("L"))
        return pytesseract.image_to_string(img, lang='por+eng')
    except Exception as e: return f"Erro OCR: {e}"

def ler_pdf(caminho):
    texto_total = ""
    try:
        doc = fitz.open(caminho)
        for i, pagina in enumerate(doc):
            t = pagina.get_text()
            # Lógica Híbrida: Se pouco texto, faz OCR na página
            if len(t.strip()) < 5 and cmd: 
                pix = pagina.get_pixmap()
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                if np.mean(np.array(img.convert("L"))) < 127: 
                    img = ImageOps.invert(img.convert("L"))
                t_ocr = pytesseract.image_to_string(img, lang='por+eng')
                texto_total += f"{t_ocr}\n"
            else:
                texto_total += f"{t}\n"
        doc.close()
        return texto_total
    except Exception as e: return f"Erro PDF: {e}"

def ler_planilha(caminho):
    try:
        if caminho.endswith('.csv'): df = pd.read_csv(caminho)
        else: df = pd.read_excel(caminho)
        return df.to_markdown(index=False)
    except Exception as e: return f"Erro Planilha (Instale 'tabulate'): {e}"
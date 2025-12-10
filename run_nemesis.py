import sys
import os
from streamlit.web import cli as stcli

def resolve_path(path):
    """Resolve caminhos para funcionar tanto em script quanto em EXE"""
    if getattr(sys, 'frozen', False):
        # Se estiver rodando como .exe (congelado)
        base_path = sys._MEIPASS
    else:
        # Se estiver rodando como script normal
        base_path = os.getcwd()
    return os.path.join(base_path, path)

if __name__ == "__main__":
    # Configura o ambiente para produção
    os.environ["STREAMLIT_GLOBAL_DEVELOPMENT_MODE"] = "false"
    
    # Define o caminho do app principal
    # Nota: Quando empacotado, o 'app.py' deve estar junto
    sys.argv = [
        "streamlit",
        "run",
        resolve_path("app.py"),
        "--global.developmentMode=false",
    ]
    
    sys.exit(stcli.main())
import sys
import os
from streamlit.web import cli as stcli

def main():
    # CONFIGURAÇÕES DE AMBIENTE (TELEMETRIA)
    # Colocamos isso no topo para garantir que o Chroma veja essa config antes de iniciar

    os.environ["ANONYMIZED_TELEMETRY"] = "False"
    
    # Configurações para o Streamlit não abrir janelas de aviso ou pedir e-mail

    os.environ["STREAMLIT_SERVER_HEADLESS"] = "true"
    os.environ["STREAMLIT_GLOBAL_DEVELOPMENT_MODE"] = "false"

    #RESOLUÇÃO DE CAMINHOS (PYINSTALLER)

    if getattr(sys, 'frozen', False):

        # Se estiver rodando como EXE (congelado)

        base_path = sys._MEIPASS
    else:
        # Se estiver rodando como script normal

        base_path = os.path.dirname(os.path.abspath(__file__))

    # Monta o caminho ABSOLUTO para o app.py

    app_path = os.path.join(base_path, 'app.py')

    # INICIALIZAÇÃO DO STREAMLIT
    # Monta o comando de execução simulando a linha de comando

    sys.argv = [
        "streamlit",
        "run",
        app_path,
        "--global.developmentMode=false",
    ]

    # Inicia o servidor
    
    sys.exit(stcli.main())

if __name__ == "__main__":
    main()
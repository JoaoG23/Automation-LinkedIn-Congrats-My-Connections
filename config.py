import os
from dotenv import load_dotenv

def load_config():
    # Carrega variáveis de ambiente com base na variável MY_ENV
    env_name = os.getenv("MY_ENV", "dev")

    # Localiza primeiro na pasta atual, com fallback para pasta pai
    diretorio_base = os.path.dirname(os.path.abspath(__file__))
    caminho_env_prod = os.path.join(diretorio_base, ".env.prod")
    caminho_env_dev = os.path.join(diretorio_base, ".env")

    if env_name == "prod":
        if os.path.exists(caminho_env_prod):
            load_dotenv(caminho_env_prod, override=True)
        else:
            load_dotenv("../.env.prod", override=True)
    else:
        if os.path.exists(caminho_env_dev):
            load_dotenv(caminho_env_dev, override=True)
        else:
            load_dotenv("../.env", override=True)

    configuracao = {
        "EMAIL": os.getenv("USER_LINKEDIN", ""),
        "PASSWORD": os.getenv("PASSWORD_LINKEDIN", ""),
        "ENV": env_name,
    }
    return configuracao


config = load_config()

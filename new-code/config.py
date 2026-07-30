import os
from dotenv import load_dotenv

def load_config():
    # Load environment variables based on MY_ENV
    env_name = os.getenv("MY_ENV", "dev")
    
    if env_name == "prod":
        load_dotenv("../.env.prod")
    else:
        load_dotenv("../.env")

    config = {
        "EMAIL": os.getenv("USER_LINKEDIN", ""),
        "PASSWORD": os.getenv("PASSWORD_LINKEDIN", ""),
        "ENV": env_name
    }
    return config

config = load_config()

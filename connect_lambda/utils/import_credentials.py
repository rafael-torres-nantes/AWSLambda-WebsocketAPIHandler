import os
from dotenv import load_dotenv

def aws_credentials():
    # Carregar variáveis de ambiente do arquivo .env
    load_dotenv()

    # Acessa as variáveis definidas
    ACESS_KEY = os.getenv('AWS_ACCESS_KEY_ID')
    SECRET_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    SESSION_TOKEN = os.getenv('AWS_SESSION_TOKEN')

    return ACESS_KEY, SECRET_KEY, SESSION_TOKEN
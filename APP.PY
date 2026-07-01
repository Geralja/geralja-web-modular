import os
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env que você colocou no src
load_dotenv('src/.env')

# Exemplo de como acessar uma chave:
# firebase_key = os.getenv('FIREBASE_API_KEY')

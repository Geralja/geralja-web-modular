import os
import logging
from flask import Flask, jsonify
from dotenv import load_dotenv
from config.firebase_config import db # Conexão centralizada

# 1. Configuração de Log (Essencial para diagnosticar erros em produção)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 2. Inicialização do App
def create_app():
    app = Flask(__name__)
    
    # Carrega variáveis de ambiente de forma segura
    load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
    
    # 3. Configurações de Segurança
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SESSION_COOKIE_SECURE'] = True # Força HTTPS
    app.config['SESSION_COOKIE_HTTPONLY'] = True # Protege contra ataques XSS
    
    # 4. Registro de Módulos (Blueprints)
    # Isso mantém o código limpo. Cada pasta tem seu próprio arquivo de rotas.
    # from auth.routes import auth_bp
    # from servicos.routes import servicos_bp
    
    # app.register_blueprint(auth_bp, url_prefix='/auth')
    # app.register_blueprint(servicos_bp, url_prefix='/servicos')

    # 5. Rota de Health Check (Monitoramento para garantir que o site não caiu)
    @app.route('/health', methods=['GET'])
    def health_check():
        return jsonify({"status": "online", "database": "connected"}), 200

    @app.route('/')
    def index():
        return "GeralJá Modular - Sistema Online"

    # 6. Tratamento de Erros Global (Evita que o site "quebre" na frente do usuário)
    @app.errorhandler(500)
    def internal_error(e):
        logger.error(f"Erro interno: {e}")
        return jsonify({"error": "Erro interno no servidor"}), 500

    return app

# Inicialização
app = create_app()

if __name__ == '__main__':
    # Em produção, você não usa 'debug=True'. 
    # Usaremos um servidor como Gunicorn para lidar com milhares de acessos.
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

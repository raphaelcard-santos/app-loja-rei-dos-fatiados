import sys
import os

# Adiciona o diretório pai de 'src' ao sys.path para permitir importações absolutas de 'src'
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from datetime import timedelta

# Importa db e bcrypt de src.models.usuario, pois db é inicializado lá agora
from src.models.usuario import db, bcrypt 
from src.routes.cliente_routes import cliente_bp
from src.routes.compra_routes import compra_bp
from src.routes.auth_routes import auth_bp # Importa a blueprint de autenticação

def create_app():
    app = Flask(__name__, static_folder='static', static_url_path='')
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', os.urandom(24)) # Chave secreta para sessões, etc.
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'super-secret-jwt') # Chave para JWT, deve ser segura e diferente em produção
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1) # Tempo de expiração do token de acesso

    # Configuração do Banco de Dados MySQL
    db_user = os.getenv('DB_USERNAME', 'root')
    db_password = os.getenv('DB_PASSWORD', 'password')
    db_host = os.getenv('DB_HOST', 'localhost')
    db_port = os.getenv('DB_PORT', '3306')
    db_name = os.getenv('DB_NAME', 'mydb')
    
    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    bcrypt.init_app(app) # Inicializa o Bcrypt com o app
    jwt = JWTManager(app) # Inicializa o JWTManager com o app

    # Callbacks para mensagens de erro do JWT personalizadas (opcional, mas bom para consistência)
    @jwt.unauthorized_loader
    def unauthorized_callback(error_string):
        return jsonify(mensagem="Acesso não autorizado. Token de acesso ausente ou inválido."), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error_string):
        return jsonify(mensagem="Token inválido."), 422 # Unprocessable Entity

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify(mensagem="Token expirou."), 401

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return jsonify(mensagem="Token foi revogado."), 401

    @jwt.needs_fresh_token_loader
    def fresh_token_callback(jwt_header, jwt_payload):
        return jsonify(mensagem="Token fresco necessário."), 401

    with app.app_context():
        db.create_all() # Cria todas as tabelas, incluindo 'usuarios'

    # Registrar Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(cliente_bp)
    app.register_blueprint(compra_bp)

    @app.route('/')
    def index():
        return "Bem-vindo ao App Rei dos Fatiados! Use /auth/register para criar uma conta e /auth/login para obter um token."

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)


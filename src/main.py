import sys
import os

# Adiciona o diretório pai de 'src' ao sys.path para permitir importações absolutas de 'src'
# Exemplo: from src.models import db
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask
from src.models.cliente import db # Importa db de src.models.cliente
from src.routes.cliente_routes import cliente_bp
from src.routes.compra_routes import compra_bp # Importa a blueprint de compras

def create_app():
    app = Flask(__name__, static_folder='static', static_url_path='')
    app.config['SECRET_KEY'] = os.urandom(24) # Chave secreta para sessões, etc.

    # Configuração do Banco de Dados MySQL
    db_user = os.getenv('DB_USERNAME', 'root')
    db_password = os.getenv('DB_PASSWORD', 'password')
    db_host = os.getenv('DB_HOST', 'localhost')
    db_port = os.getenv('DB_PORT', '3306')
    db_name = os.getenv('DB_NAME', 'mydb')
    
    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()

    # Registrar Blueprints
    app.register_blueprint(cliente_bp)
    app.register_blueprint(compra_bp) # Registra a blueprint de compras

    @app.route('/')
    def index():
        return "Bem-vindo ao App Rei dos Fatiados!"

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)


from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from src.models.usuario import Usuario, db, bcrypt

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/register", methods=["POST"])
def register_user():
    data = request.get_json()
    email = data.get("email")
    senha = data.get("senha")

    if not email or not senha:
        return jsonify({"mensagem": "Email e senha são obrigatórios"}), 400

    if Usuario.query.filter_by(email=email).first():
        return jsonify({"mensagem": "Usuário já cadastrado com este email"}), 409

    novo_usuario = Usuario(email=email, senha=senha)
    db.session.add(novo_usuario)
    db.session.commit()

    return jsonify({"mensagem": "Usuário registrado com sucesso!", "usuario_id": novo_usuario.id}), 201

@auth_bp.route("/login", methods=["POST"])
def login_user():
    data = request.get_json()
    email = data.get("email")
    senha = data.get("senha")

    if not email or not senha:
        return jsonify({"mensagem": "Email e senha são obrigatórios"}), 400

    usuario = Usuario.query.filter_by(email=email).first()

    if usuario and usuario.verificar_senha(senha):
        access_token = create_access_token(identity=usuario.id)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"mensagem": "Credenciais inválidas"}), 401


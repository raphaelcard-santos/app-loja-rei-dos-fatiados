from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from src.models.cliente import Cliente, db

cliente_bp = Blueprint("cliente_bp", __name__, url_prefix="/clientes")

@cliente_bp.route("/", methods=["POST"])
@jwt_required()
def criar_cliente():
    dados = request.get_json()
    novo_cliente = Cliente(nome=dados.get("nome"), telefone=dados.get("telefone"), email=dados.get("email"))
    db.session.add(novo_cliente)
    db.session.commit()
    return jsonify({"mensagem": "Cliente criado com sucesso!", "id": novo_cliente.id}), 201

@cliente_bp.route("/", methods=["GET"])
@jwt_required()
def listar_clientes():
    clientes = Cliente.query.all()
    return jsonify([{"id": c.id, "nome": c.nome, "telefone": c.telefone, "email": c.email, "data_cadastro": c.data_cadastro.isoformat()} for c in clientes])

@cliente_bp.route("/<int:cliente_id>", methods=["GET"])
@jwt_required()
def detalhar_cliente(cliente_id):
    cliente = Cliente.query.get_or_404(cliente_id)
    return jsonify({
        "id": cliente.id, 
        "nome": cliente.nome, 
        "telefone": cliente.telefone, 
        "email": cliente.email, 
        "data_cadastro": cliente.data_cadastro.isoformat()
    })

@cliente_bp.route("/<int:cliente_id>", methods=["PUT"])
@jwt_required()
def atualizar_cliente(cliente_id):
    cliente = Cliente.query.get_or_404(cliente_id)
    dados = request.get_json()
    cliente.nome = dados.get("nome", cliente.nome)
    cliente.telefone = dados.get("telefone", cliente.telefone)
    cliente.email = dados.get("email", cliente.email)
    db.session.commit()
    return jsonify({"mensagem": "Cliente atualizado com sucesso!"})

@cliente_bp.route("/<int:cliente_id>", methods=["DELETE"])
@jwt_required()
def deletar_cliente(cliente_id):
    cliente = Cliente.query.get_or_404(cliente_id)
    # Adicionar lógica para verificar se o cliente tem compras antes de deletar, se necessário
    # ou configurar o banco de dados para deletar em cascata (se apropriado)
    # Por enquanto, apenas deleta o cliente.
    # Para deletar compras associadas, seria necessário buscar e deletar Compra.query.filter_by(cliente_id=cliente_id).delete()
    db.session.delete(cliente)
    db.session.commit()
    return jsonify({"mensagem": "Cliente deletado com sucesso!"})


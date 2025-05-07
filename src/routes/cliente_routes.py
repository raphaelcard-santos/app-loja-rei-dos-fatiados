from flask import Blueprint, request, jsonify
from src.models.cliente import Cliente, db

cliente_bp = Blueprint('cliente_bp', __name__, url_prefix='/clientes')

@cliente_bp.route('/', methods=['POST'])
def criar_cliente():
    dados = request.get_json()
    novo_cliente = Cliente(nome=dados.get('nome'), telefone=dados.get('telefone'), email=dados.get('email'))
    db.session.add(novo_cliente)
    db.session.commit()
    return jsonify({'mensagem': 'Cliente criado com sucesso!', 'id': novo_cliente.id}), 201

@cliente_bp.route('/', methods=['GET'])
def listar_clientes():
    clientes = Cliente.query.all()
    return jsonify([{'id': c.id, 'nome': c.nome, 'telefone': c.telefone, 'email': c.email, 'data_cadastro': c.data_cadastro} for c in clientes])

@cliente_bp.route('/<int:cliente_id>', methods=['GET'])
def detalhar_cliente(cliente_id):
    cliente = Cliente.query.get_or_404(cliente_id)
    return jsonify({'id': cliente.id, 'nome': cliente.nome, 'telefone': cliente.telefone, 'email': cliente.email, 'data_cadastro': cliente.data_cadastro})

@cliente_bp.route('/<int:cliente_id>', methods=['PUT'])
def atualizar_cliente(cliente_id):
    cliente = Cliente.query.get_or_404(cliente_id)
    dados = request.get_json()
    cliente.nome = dados.get('nome', cliente.nome)
    cliente.telefone = dados.get('telefone', cliente.telefone)
    cliente.email = dados.get('email', cliente.email)
    db.session.commit()
    return jsonify({'mensagem': 'Cliente atualizado com sucesso!'})

@cliente_bp.route('/<int:cliente_id>', methods=['DELETE'])
def deletar_cliente(cliente_id):
    cliente = Cliente.query.get_or_404(cliente_id)
    db.session.delete(cliente)
    db.session.commit()
    return jsonify({'mensagem': 'Cliente deletado com sucesso!'})


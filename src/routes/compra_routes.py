from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required # Importar jwt_required
from src.models.compra import Compra, db
from src.models.cliente import Cliente # Para verificar se o cliente existe
import datetime
from sqlalchemy import func, and_
from decimal import Decimal # Para precisão monetária

compra_bp = Blueprint("compra_bp", __name__, url_prefix=	"/compras")

@compra_bp.route("/cliente/<int:cliente_id>", methods=["POST"])
@jwt_required() # Proteger rota
def criar_compra(cliente_id):
    cliente = Cliente.query.get_or_404(cliente_id)
    dados = request.get_json()
    
    try:
        valor_total = Decimal(dados.get("valor_total"))
        valor_pago = Decimal(dados.get("valor_pago", "0.0"))
    except Exception:
        return jsonify({"mensagem": "Valor total e valor pago devem ser números válidos."}), 400

    if valor_pago > valor_total:
        return jsonify({"mensagem": "Valor pago não pode ser maior que o valor total."}), 400

    nova_compra = Compra(
        cliente_id=cliente_id,
        descricao=dados.get("descricao"),
        valor_total=valor_total,
        valor_pago=valor_pago,
        mes_referencia=dados.get("mes_referencia", datetime.datetime.utcnow().month),
        ano_referencia=dados.get("ano_referencia", datetime.datetime.utcnow().year)
    )
    db.session.add(nova_compra)
    db.session.commit()
    return jsonify({"mensagem": "Compra registrada com sucesso!", "id": nova_compra.id}), 201

@compra_bp.route("/cliente/<int:cliente_id>", methods=["GET"])
@jwt_required() # Proteger rota
def listar_compras_cliente(cliente_id):
    Cliente.query.get_or_404(cliente_id) # Garante que o cliente existe
    compras = Compra.query.filter_by(cliente_id=cliente_id).order_by(Compra.data_compra.desc()).all()
    return jsonify([{
        "id": c.id, 
        "descricao": c.descricao, 
        "valor_total": str(c.valor_total), 
        "valor_pago": str(c.valor_pago),
        "saldo_devedor": str(c.saldo_devedor),
        "status_pagamento": c.status_pagamento,
        "data_compra": c.data_compra.isoformat() if c.data_compra else None,
        "mes_referencia": c.mes_referencia,
        "ano_referencia": c.ano_referencia,
        "encerrada": c.encerrada
    } for c in compras])

@compra_bp.route("/<int:compra_id>", methods=["GET"])
@jwt_required() # Proteger rota
def detalhar_compra(compra_id):
    compra = Compra.query.get_or_404(compra_id)
    return jsonify({
        "id": compra.id, 
        "cliente_id": compra.cliente_id,
        "descricao": compra.descricao, 
        "valor_total": str(compra.valor_total), 
        "valor_pago": str(compra.valor_pago),
        "saldo_devedor": str(compra.saldo_devedor),
        "status_pagamento": compra.status_pagamento,
        "data_compra": compra.data_compra.isoformat() if compra.data_compra else None,
        "mes_referencia": compra.mes_referencia,
        "ano_referencia": compra.ano_referencia,
        "encerrada": compra.encerrada
    })

@compra_bp.route("/<int:compra_id>/pagar", methods=["POST"])
@jwt_required() # Proteger rota
def registrar_pagamento(compra_id):
    compra = Compra.query.get_or_404(compra_id)
    dados = request.get_json()
    
    if compra.encerrada:
        return jsonify({"mensagem": "Não é possível registrar pagamento para uma compra encerrada."}), 400

    try:
        valor_pagamento = Decimal(dados.get("valor_pagamento"))
    except Exception:
        return jsonify({"mensagem": "Valor do pagamento deve ser um número válido."}), 400

    if valor_pagamento <= 0:
        return jsonify({"mensagem": "Valor do pagamento deve ser positivo."}), 400

    novo_valor_pago = compra.valor_pago + valor_pagamento
    
    if novo_valor_pago > compra.valor_total:
        return jsonify({"mensagem": f"Pagamento de R${valor_pagamento:.2f} excede o saldo devedor de R${compra.saldo_devedor:.2f}."}), 400
        
    compra.valor_pago = novo_valor_pago
    db.session.commit()
    return jsonify({
        "mensagem": "Pagamento registrado com sucesso!",
        "id": compra.id,
        "novo_valor_pago": str(compra.valor_pago),
        "saldo_devedor": str(compra.saldo_devedor),
        "status_pagamento": compra.status_pagamento
    })

@compra_bp.route("/<int:compra_id>", methods=["PUT"])
@jwt_required() # Proteger rota
def atualizar_compra(compra_id):
    compra = Compra.query.get_or_404(compra_id)
    dados = request.get_json()

    if compra.encerrada:
        return jsonify({"mensagem": "Não é possível atualizar uma compra encerrada."}), 400

    compra.descricao = dados.get("descricao", compra.descricao)
    novo_valor_total_str = dados.get("valor_total")
    novo_valor_pago_str = dados.get("valor_pago")

    if novo_valor_total_str is not None:
        try:
            compra.valor_total = Decimal(novo_valor_total_str)
        except Exception:
            return jsonify({"mensagem": "Valor total deve ser um número válido."}), 400

    if novo_valor_pago_str is not None:
        try:
            valor_pago_decimal = Decimal(novo_valor_pago_str)
            if valor_pago_decimal > compra.valor_total:
                 return jsonify({"mensagem": "Valor pago não pode ser maior que o valor total."}), 400
            compra.valor_pago = valor_pago_decimal
        except Exception:
            return jsonify({"mensagem": "Valor pago deve ser um número válido."}), 400
    
    if compra.valor_pago > compra.valor_total:
        compra.valor_pago = compra.valor_total

    db.session.commit()
    return jsonify({
        "mensagem": "Compra atualizada com sucesso!", 
        "id": compra.id,
        "valor_total": str(compra.valor_total),
        "valor_pago": str(compra.valor_pago),
        "saldo_devedor": str(compra.saldo_devedor)
    })

@compra_bp.route("/<int:compra_id>", methods=["DELETE"])
@jwt_required() # Proteger rota
def deletar_compra(compra_id):
    compra = Compra.query.get_or_404(compra_id)
    if compra.encerrada:
        return jsonify({"mensagem": "Não é possível deletar uma compra encerrada."}), 400
    if compra.valor_pago > 0:
        return jsonify({"mensagem": "Não é possível deletar uma compra que já possui pagamentos registrados."}), 400
    
    db.session.delete(compra)
    db.session.commit()
    return jsonify({"mensagem": "Compra deletada com sucesso!"})


@compra_bp.route("/fechamento_mensal", methods=["POST"])
@jwt_required() # Proteger rota
def fechamento_mensal():
    dados = request.get_json()
    mes = dados.get("mes")
    ano = dados.get("ano")

    if not mes or not ano:
        return jsonify({"mensagem": "Mês e ano são obrigatórios para o fechamento."}), 400
    
    try:
        mes = int(mes)
        ano = int(ano)
        if not (1 <= mes <= 12):
            raise ValueError("Mês inválido")
    except ValueError as e:
        return jsonify({"mensagem": f"Mês ou ano inválido: {e}"}), 400

    clientes = Cliente.query.all()
    log_fechamento = []

    for cliente in clientes:
        compras_do_mes = Compra.query.filter(
            Compra.cliente_id == cliente.id,
            Compra.mes_referencia == mes,
            Compra.ano_referencia == ano,
            Compra.encerrada == False
        ).all()

        saldo_devedor_total_mes = Decimal("0.00")
        compras_encerradas_cliente = 0

        for compra_item in compras_do_mes:
            saldo_devedor_total_mes += compra_item.saldo_devedor
            compra_item.encerrada = True
            compras_encerradas_cliente += 1
        
        if saldo_devedor_total_mes > Decimal("0.00"):
            # Calcular próximo mês e ano
            proximo_mes = mes + 1
            proximo_ano = ano
            if proximo_mes > 12:
                proximo_mes = 1
                proximo_ano += 1
            
            nova_compra_saldo = Compra(
                cliente_id=cliente.id,
                descricao=f"Saldo devedor referente a {mes:02d}/{ano}",
                valor_total=saldo_devedor_total_mes,
                valor_pago=Decimal("0.00"),
                mes_referencia=proximo_mes,
                ano_referencia=proximo_ano,
                data_compra=datetime.datetime(proximo_ano, proximo_mes, 1) # Início do próximo mês
            )
            db.session.add(nova_compra_saldo)
            log_fechamento.append(f"Cliente {cliente.id} ({cliente.nome}): Saldo de R${saldo_devedor_total_mes:.2f} transferido para {proximo_mes:02d}/{proximo_ano}. {compras_encerradas_cliente} compras encerradas.")
        elif compras_encerradas_cliente > 0:
            log_fechamento.append(f"Cliente {cliente.id} ({cliente.nome}): {compras_encerradas_cliente} compras encerradas sem saldo devedor.")
        # else: cliente sem compras no período ou já encerradas

    if not log_fechamento and not Compra.query.filter(Compra.mes_referencia == mes, Compra.ano_referencia == ano, Compra.encerrada == False).first():
        return jsonify({"mensagem": f"Nenhuma compra aberta encontrada para fechamento em {mes:02d}/{ano}."}), 200

    db.session.commit()
    return jsonify({"mensagem": f"Fechamento do mês {mes:02d}/{ano} concluído.", "detalhes": log_fechamento}), 200


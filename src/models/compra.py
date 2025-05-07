from sqlalchemy.sql import func
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from src.models.cliente import db # Importa a instância db de cliente.py
import datetime

class Compra(db.Model):
    __tablename__ = 'compra'
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    descricao = db.Column(db.String(255), nullable=False)
    valor_total = db.Column(db.Numeric(10, 2), nullable=False)
    valor_pago = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)
    data_compra = db.Column(db.DateTime(timezone=True), server_default=func.now())
    mes_referencia = db.Column(db.Integer, nullable=False, default=datetime.datetime.utcnow().month)
    ano_referencia = db.Column(db.Integer, nullable=False, default=datetime.datetime.utcnow().year)
    encerrada = db.Column(db.Boolean, default=False, nullable=False) # Para controle de fechamento mensal
    saldo_mes_seguinte = db.Column(db.Numeric(10, 2), nullable=True) # Saldo transferido para o próximo mês

    # Relacionamento com Cliente (opcional, já que cliente_id está aqui)
    # cliente = relationship("Cliente", back_populates="compras")

    @property
    def saldo_devedor(self):
        return self.valor_total - self.valor_pago

    @property
    def status_pagamento(self):
        if self.valor_pago >= self.valor_total:
            return "Pago Totalmente"
        elif self.valor_pago > 0:
            return "Pago Parcialmente"
        else:
            return "Pendente"

    def __repr__(self):
        return f'<Compra {self.id} - Cliente {self.cliente_id} - Valor {self.valor_total}>'

# Atualizar o modelo Cliente para incluir o relacionamento com Compras
# Isso será feito editando o arquivo cliente.py


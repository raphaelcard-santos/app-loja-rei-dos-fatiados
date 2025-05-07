from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship # Adicionado para o relacionamento

db = SQLAlchemy()

class Cliente(db.Model):
    __tablename__ = 'cliente'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(100), nullable=True, unique=True)
    data_cadastro = db.Column(db.DateTime(timezone=True), server_default=func.now())
    
    # Relacionamento com Compras: um cliente pode ter várias compras
    compras = db.relationship('Compra', backref='cliente', lazy='dynamic', cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Cliente {self.nome}>'


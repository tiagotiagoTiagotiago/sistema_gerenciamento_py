from flask import jsonify, request
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    preco = db.Column(db.Numeric(10, 2), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)  # 'ativo' ou 'passivo'

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'quantidade': self.quantidade,
            'preco': float(self.preco),
            'tipo': self.tipo
        }

def get_produtos():
    produtos = Produto.query.all()
    produtos_list = [produto.to_dict() for produto in produtos]
    return jsonify(produtos_list)

def get_produto(id):
    produto = Produto.query.get_or_404(id)
    return jsonify(produto.to_dict())

def create_produto():
    new_produto = request.get_json()
    produto = Produto(
        nome=new_produto['nome'],
        quantidade=new_produto['quantidade'],
        preco=new_produto['preco'],
        tipo=new_produto['tipo']
    )
    db.session.add(produto)
    db.session.commit()
    return jsonify({'id': produto.id}), 201

def update_produto(id):
    produto = Produto.query.get_or_404(id)
    updated_produto = request.get_json()
    produto.nome = updated_produto['nome']
    produto.quantidade = updated_produto['quantidade']
    produto.preco = updated_produto['preco']
    produto.tipo = updated_produto['tipo']
    db.session.commit()
    return jsonify({'message': 'Produto atualizado'})

def delete_produto(id):
    produto = Produto.query.get_or_404(id)
    db.session.delete(produto)
    db.session.commit()
    return jsonify({'message': 'Produto deletado'})

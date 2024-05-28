from flask import jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Emprestimo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    funcionario_id = db.Column(db.Integer, db.ForeignKey('funcionario.id'), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey('produto.id'), nullable=False)
    data_emprestimo = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    data_devolucao = db.Column(db.DateTime, nullable=True)

    funcionario = db.relationship('Funcionario', backref='emprestimos')
    produto = db.relationship('Produto', backref='emprestimos')

    def to_dict(self):
        return {
            'id': self.id,
            'funcionario_id': self.funcionario_id,
            'produto_id': self.produto_id,
            'data_emprestimo': self.data_emprestimo.isoformat(),
            'data_devolucao': self.data_devolucao.isoformat() if self.data_devolucao else None
        }

def get_emprestimos():
    emprestimos = Emprestimo.query.all()
    emprestimos_list = [emprestimo.to_dict() for emprestimo in emprestimos]
    return jsonify(emprestimos_list)

def get_emprestimo(id):
    emprestimo = Emprestimo.query.get_or_404(id)
    return jsonify(emprestimo.to_dict())

def create_emprestimo():
    new_emprestimo = request.get_json()
    emprestimo = Emprestimo(
        funcionario_id=new_emprestimo['funcionario_id'],
        produto_id=new_emprestimo['produto_id']
    )
    db.session.add(emprestimo)
    db.session.commit()
    return jsonify({'id': emprestimo.id}), 201

def update_emprestimo(id):
    emprestimo = Emprestimo.query.get_or_404(id)
    updated_emprestimo = request.get_json()
    emprestimo.data_devolucao = updated_emprestimo.get('data_devolucao')
    db.session.commit()
    return jsonify({'message': 'Empréstimo atualizado'})

def delete_emprestimo(id):
    emprestimo = Emprestimo.query.get_or_404(id)
    db.session.delete(emprestimo)
    db.session.commit()
    return jsonify({'message': 'Empréstimo deletado'})

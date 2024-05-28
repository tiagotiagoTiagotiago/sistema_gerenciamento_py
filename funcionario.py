from flask import jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Funcionario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cargo = db.Column(db.String(100), nullable=False)
 

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'cargo': self.cargo,
        }

def get_funcionarios():
    funcionarios = Funcionario.query.all()
    funcionarios_list = [funcionario.to_dict() for funcionario in funcionarios]
    return jsonify(funcionarios_list)

def get_funcionario(id):
    funcionario = Funcionario.query.get_or_404(id)
    return jsonify(funcionario.to_dict())

def create_funcionario():
    new_funcionario = request.get_json()
    funcionario = Funcionario(
        nome=new_funcionario['nome'],
        cargo=new_funcionario['cargo'],
      
    )
    db.session.add(funcionario)
    db.session.commit()
    return jsonify({'id': funcionario.id}), 201

def update_funcionario(id):
    funcionario = Funcionario.query.get_or_404(id)
    updated_funcionario = request.get_json()
    funcionario.nome = updated_funcionario['nome']
    funcionario.cargo = updated_funcionario['cargo']
  
    db.session.commit()
    return jsonify({'message': 'Funcionário atualizado'})

def delete_funcionario(id):
    funcionario = Funcionario.query.get_or_404(id)
    db.session.delete(funcionario)
    db.session.commit()
    return jsonify({'message': 'Funcionário deletado'})

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:tiagobarbosa@localhost/estoque_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    preco = db.Column(db.Numeric(10, 2), nullable=False)

class Funcionario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cargo = db.Column(db.String(100), nullable=False)
    
class Emprestimo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    funcionario_id = db.Column(db.Integer, db.ForeignKey('funcionario.id'), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey('produto.id'), nullable=False)
    data_emprestimo = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    data_devolucao = db.Column(db.DateTime, nullable=True)
    funcionario = db.relationship('Funcionario', backref=db.backref('emprestimos', lazy=True))
    produto = db.relationship('Produto', backref=db.backref('emprestimos', lazy=True))

@app.route('/produtos', methods=['GET'])
def get_produtos():
    produtos = Produto.query.all()
    produtos_list = [{
        'id': produto.id,
        'nome': produto.nome,
        'quantidade': produto.quantidade,
        'preco': float(produto.preco)
    } for produto in produtos]
    return jsonify(produtos_list)

@app.route('/produto/<int:id>', methods=['GET'])
def get_produto(id):
    produto = Produto.query.get_or_404(id)
    produto_data = {
        'id': produto.id,
        'nome': produto.nome,
        'quantidade': produto.quantidade,
        'preco': produto.preco
    }
    return jsonify(produto_data)


@app.route('/produtos', methods=['POST'])
def create_produto():
    new_produto = request.get_json()
    produto = Produto(
        nome=new_produto['nome'],
        quantidade=new_produto['quantidade'],
        preco=new_produto['preco']
    )
    db.session.add(produto)
    db.session.commit()
    return jsonify({'id': produto.id}), 201

@app.route('/produtos/<int:id>', methods=['PUT'])
def update_produto(id):
    produto = Produto.query.get_or_404(id)
    updated_produto = request.get_json()
    produto.nome = updated_produto['nome']
    produto.quantidade = updated_produto['quantidade']
    produto.preco = updated_produto['preco']
    db.session.commit()
    return jsonify({'message': 'Produto atualizado'})

@app.route('/produtos/<int:id>', methods=['DELETE'])
def delete_produto(id):
    produto = Produto.query.get_or_404(id)
    db.session.delete(produto)
    db.session.commit()
    return jsonify({'message': 'Produto deletado'})

@app.route('/funcionarios', methods=['GET'])
def get_funcionarios():
    funcionarios = Funcionario.query.all()
    funcionarios_list = [{
        'id': funcionario.id,
        'nome': funcionario.nome,
        'cargo': funcionario.cargo,
       
    } for funcionario in funcionarios]
    return jsonify(funcionarios_list)

@app.route('/funcionario/<int:id>', methods=['GET'])
def get_funcionario(id):
    funcionario = Funcionario.query.get_or_404(id)
    funcionario_data = {
        'id': funcionario.id,
        'nome': funcionario.nome,
        'cargo': funcionario.cargo,
      
    }
    return jsonify(funcionario_data)


@app.route('/funcionarios', methods=['POST'])
def create_funcionario():
    new_funcionario = request.get_json()
    funcionario = Funcionario(
        nome=new_funcionario['nome'],
        cargo=new_funcionario['cargo'],
    
    )
    db.session.add(funcionario)
    db.session.commit()
    return jsonify({'id': funcionario.id}), 201

@app.route('/funcionario/<int:id>', methods=['PUT'])
def update_funcionario(id):
    funcionario = Funcionario.query.get_or_404(id)
    updated_funcionario = request.get_json()
    funcionario.nome = updated_funcionario['nome']
    funcionario.cargo = updated_funcionario['cargo']
   
    db.session.commit()
    return jsonify({'message': 'Funcionario atualizado'})

@app.route('/funcionario/<int:id>', methods=['DELETE'])
def delete_funcionario(id):
    funcionario = Funcionario.query.get_or_404(id)
    db.session.delete(funcionario)
    db.session.commit()
    return jsonify({'message': 'Funcionario deletado'})


@app.route('/emprestimos', methods=['POST'])
def create_emprestimo():
    data = request.get_json()
    emprestimo = Emprestimo(
        funcionario_id=data['funcionario_id'],
        produto_id=data['produto_id']
    )
    db.session.add(emprestimo)
    db.session.commit()
    return jsonify({'id': emprestimo.id}), 201

@app.route('/emprestimos', methods=['GET'])
def get_emprestimos():
    emprestimos = Emprestimo.query.all()
    emprestimos_list = [{
        'id': emprestimo.id,
        'funcionario_id': emprestimo.funcionario_id,
        'produto_id': emprestimo.produto_id,
        'data_emprestimo': emprestimo.data_emprestimo.isoformat(),
        'data_devolucao': emprestimo.data_devolucao.isoformat() if emprestimo.data_devolucao else None
    } for emprestimo in emprestimos]
    return jsonify(emprestimos_list)

@app.route('/emprestimos/<int:id>', methods=['PUT'])
def update_emprestimo(id):
    emprestimo = Emprestimo.query.get_or_404(id)
    data = request.get_json()
    emprestimo.data_devolucao = datetime.fromisoformat(data['data_devolucao']) if 'data_devolucao' in data else emprestimo.data_devolucao
    db.session.commit()
    return jsonify({'message': 'Emprestimo atualizado'})

@app.route('/emprestimos/<int:id>', methods=['DELETE'])
def delete_emprestimo(id):
    emprestimo = Emprestimo.query.get_or_404(id)
    db.session.delete(emprestimo)
    db.session.commit()
    return jsonify({'message': 'Emprestimo deletado'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Indicador(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    categoria = db.Column(db.String(50), nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "valor": self.valor,
            "categoria": self.categoria,
            "data_criacao": self.data_criacao
        }

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/indicadores', methods=['POST'])
def criar_indicador():
    data = request.json
    novo = Indicador(
        nome=data['nome'],
        valor=data['valor'],
        categoria=data['categoria']
    )
    db.session.add(novo)
    db.session.commit()
    return jsonify(novo.to_dict()), 201

@app.route('/indicadores', methods=['GET'])
def listar_indicadores():
    indicadores = Indicador.query.all()
    return jsonify([i.to_dict() for i in indicadores])

@app.route('/dashboard', methods=['GET'])
def dashboard():
    total = db.session.query(db.func.sum(Indicador.valor)).scalar()
    quantidade = Indicador.query.count()
    return jsonify({
        "total_valores": total or 0,
        "quantidade_indicadores": quantidade
    })

if __name__ == '__main__':
    app.run(debug=True)

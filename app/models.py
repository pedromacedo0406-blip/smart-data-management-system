from datetime import datetime
from .extensions import db

class Indicador(db.Model):
    __tablename__ = "indicadores"

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
            "data_criacao": self.data_criacao.isoformat()
        }

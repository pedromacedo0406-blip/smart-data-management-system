from flask import Blueprint, request, jsonify
from .models import Indicador
from .extensions import db

api = Blueprint("api", __name__)

@api.route("/indicadores", methods=["POST"])
def criar_indicador():
    data = request.json

    novo = Indicador(
        nome=data["nome"],
        valor=data["valor"],
        categoria=data["categoria"]
    )

    db.session.add(novo)
    db.session.commit()

    return jsonify(novo.to_dict()), 201


@api.route("/indicadores", methods=["GET"])
def listar_indicadores():
    indicadores = Indicador.query.all()
    return jsonify([i.to_dict() for i in indicadores])


@api.route("/dashboard", methods=["GET"])
def dashboard():
    total = db.session.query(db.func.sum(Indicador.valor)).scalar()
    quantidade = Indicador.query.count()

    return jsonify({
        "total_valores": total or 0,
        "quantidade_indicadores": quantidade
    })

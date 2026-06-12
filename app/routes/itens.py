"""
Blueprint de Controle de Itens.
Gerencia as operacões de criacão, leitura e exclusão dos itens no banco Supabase.
"""

from flask import Blueprint, request, jsonify
from app.models import Item
from app.database import db

itens_bp = Blueprint("itens", __name__)

# ROTA: Cadastrar Item
@itens_bp.route("/itens", methods=["POST"])
def cadastrar_item():
    dados = request.get_json()

    # Validação de Segurança
    if not dados or "uid" not in dados or "nome" not in dados or "obrigatorio" not in dados:
        return jsonify({"erro": "Campos 'uid', 'nome' e 'obrigatorio' são obrigatórios."}), 400

    uid = dados["uid"]
    nome = dados["nome"]
    obrigatorio = dados["obrigatorio"]

    # Impedimento de Duplicidade
    if Item.query.filter_by(uid=uid).first():
        return jsonify({"erro": "Já existe um item cadastrado com este UID."}), 409

    # Persistência de Dados
    novo_item = Item(uid=uid, nome=nome, obrigatorio=obrigatorio)
    db.session.add(novo_item)
    db.session.commit()

    return jsonify({
        "mensagem": "Item cadastrado com sucesso.",
        "item": {"uid": uid, "nome": nome, "obrigatorio": obrigatorio}
    }), 201

# ROTA: Listar Itens
@itens_bp.route("/itens", methods=["GET"])
def listar_itens():
    itens = Item.query.all()
    lista = [{"uid": i.uid, "nome": i.nome, "obrigatorio": i.obrigatorio} for i in itens]
    return jsonify({"itens": lista, "total": len(lista)}), 200

# ROTA: Editar Item
@itens_bp.route("/itens/<uid>", methods=["PATCH"])
def editar_item(uid):
    item = Item.query.filter_by(uid=uid).first()

    if not item:
        return jsonify({"erro": f"Item com UID '{uid}' não encontrado."}), 404

    dados = request.get_json()

    # Validações de Segurança
    if not dados or ("nome" not in dados and "obrigatorio" not in dados):
        return jsonify({"erro": "Informe ao menos um campo para editar: 'nome' ou 'obrigatorio'."}), 400
    if "uid" in dados:
        return jsonify({"erro": "O campo 'uid' não pode ser alterado."}), 400

    # Aplicação das Alterações
    if "nome" in dados:
        item.nome = dados["nome"]
    if "obrigatorio" in dados:
        item.obrigatorio = dados["obrigatorio"]

    db.session.commit()

    return jsonify({
        "mensagem": "Item atualizado com sucesso.",
        "item": {"uid": item.uid, "nome": item.nome, "obrigatorio": item.obrigatorio}
    }), 200

# ROTA: Remover Item por UID
@itens_bp.route("/itens/<uid>", methods=["DELETE"])
def remover_item(uid):
    item = Item.query.filter_by(uid=uid).first()

    if not item:
        return jsonify({"erro": f"Item com UID '{uid}' não encontrado."}), 404

    db.session.delete(item)
    db.session.commit()
    return jsonify({"mensagem": "Item removido com sucesso.", "uid": uid}), 200
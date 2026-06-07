"""
Módulo de Processamento e Verificação de Itens.
Valida as leituras enviadas pelo leitor Raspberry e gerencia notificações em caso de itens obrigatórios ausentes.
"""

from flask import Blueprint, request, jsonify
from app.models import Item
from app.services.onesignal import enviar_notificacao

processar_bp = Blueprint("processar", __name__)

# ROTA: Processar Leituras e Validar Itens
@processar_bp.route("/processar", methods=["POST"])
def processar():
    dados = request.get_json()

    # Validação de Segurança
    if not dados or "uids_lidos" not in dados:
        return jsonify({"erro": "O campo 'uids_lidos' é obrigatório."}), 400

    uids_lidos = dados["uids_lidos"]

    # Consulta de Regras de Negócio no Banco de Dados
    itens_obrigatorios = Item.query.filter_by(obrigatorio=True).all()

    # Filtro de Itens Ausentes
    itens_faltando = [
        {"uid": item.uid, "nome": item.nome}
        for item in itens_obrigatorios
        if item.uid not in uids_lidos
    ]

    if itens_faltando:
        quantidade = len(itens_faltando)

        # Formatação Dinâmica de Texto
        mensagem = (
            f"{quantidade} item obrigatório não foi encontrado."
            if quantidade == 1
            else f"{quantidade} itens obrigatórios não foram encontrados."
        )

        # Disparo do Alerta para o OneSignal
        enviar_notificacao(mensagem)
        return jsonify({
            "status": "alerta",
            "itens_faltando": itens_faltando,
            "mensagem": mensagem
        }), 200

    return jsonify({
        "status": "ok",
        "itens_faltando": [],
        "mensagem": "Todos os itens obrigatórios estão presentes."
    }), 200
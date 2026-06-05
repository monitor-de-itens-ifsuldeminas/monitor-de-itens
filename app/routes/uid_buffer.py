"""
Blueprint de Buffer de UIDs.
Gerencia o fluxo temporário de UIDs capturados pelo leitor Raspberry e consumidos pelo aplicativo.
"""

from flask import Blueprint, request, jsonify
from app.models import UidBuffer
from app.database import db
from datetime import datetime, timezone

uid_buffer_bp = Blueprint("uid_buffer", __name__)

# ROTA: Cadastrar UID
@uid_buffer_bp.route("/cadastrar-uid", methods=["POST"])
def cadastrar_uid():
    dados = request.get_json()

    # Validação de Segurança
    if not dados or "uid" not in dados:
        return jsonify({"erro": "O campo 'uid' é obrigatório."}), 400

    uid = dados["uid"]

    # Registro Temporal em Fuso Horário Global (UTC)
    entrada = UidBuffer(uid=uid, lido_em=datetime.now(timezone.utc))
    db.session.add(entrada)
    db.session.commit()

    return jsonify({
        "mensagem": "UID recebido e armazenado com sucesso.",
        "uid": uid
    }), 200

# ROTA: Ler UID
@uid_buffer_bp.route("/ler-uid", methods=["GET"])
def ler_uid():
    # Captura do Parâmetro de Controle Temporal
    desde_str = request.args.get("desde")

    if desde_str:
        try:
            # Tratamento de String e Conversão de Fuso Horário
            desde = datetime.fromisoformat(desde_str.replace("Z", "+00:00"))

            # Busca Inteligente pela Primeira Leitura Pós-Clique
            entrada = (
                UidBuffer.query
                .filter(UidBuffer.lido_em > desde)
                .order_by(UidBuffer.lido_em.asc())
                .first()
            )
        # Tratamento de Erro para Formatação de Data Inválida
        except ValueError:
            return jsonify({"erro": "Formato de 'desde' inválido. Use ISO 8601."}), 400
    else:
        # Fallback de Compatibilidade
        entrada = UidBuffer.query.order_by(UidBuffer.lido_em.desc()).first()

    if not entrada:
        return jsonify({"uid": None, "status": "aguardando"}), 200

    return jsonify({"uid": entrada.uid, "status": "disponivel"}), 200
from flask import Blueprint, request, jsonify

processar_bp = Blueprint("processar", __name__)

ITENS_MOCK = [
    {"uid": "E2003412B802011833303632", "nome": "Chave de Casa",  "obrigatorio": True},
    {"uid": "E2003412B802011833303633", "nome": "Carteira",       "obrigatorio": True},
    {"uid": "E2003412B802011833303634", "nome": "Crachá IFSUL",   "obrigatorio": True},
    {"uid": "E2003412B802011833303635", "nome": "Chave do Carro", "obrigatorio": False},
]

@processar_bp.route("/processar", methods=["POST"])
def processar():
    dados = request.get_json()

    if not dados or "uids_lidos" not in dados:
        return jsonify({"erro": "O campo 'uids_lidos' é obrigatório."}), 400

    uids_lidos = dados["uids_lidos"]

    itens_obrigatorios = [item for item in ITENS_MOCK if item["obrigatorio"]]

    itens_faltando = [
        {"uid": item["uid"], "nome": item["nome"]}
        for item in itens_obrigatorios
        if item["uid"] not in uids_lidos
    ]

    if itens_faltando:
        quantidade = len(itens_faltando)
        mensagem = f"{quantidade} item obrigatório não foi encontrado." if quantidade == 1 \
                   else f"{quantidade} itens obrigatórios não foram encontrados."
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
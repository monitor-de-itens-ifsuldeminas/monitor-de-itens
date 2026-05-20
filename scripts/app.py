from flask import Flask, jsonify

app = Flask(__name__)

# ── Mock de dados ────────────────────────────────────────────────────────────
ITENS_MOCK = [
    {"uid": "E2003412B802011833303632", "nome": "Chave de Casa",    "obrigatorio": True},
    {"uid": "E2003412B802011833303633", "nome": "Carteira",         "obrigatorio": True},
    {"uid": "E2003412B802011833303634", "nome": "Crachá IFSUL",     "obrigatorio": True},
    {"uid": "E2003412B802011833303635", "nome": "Chave do Carro",   "obrigatorio": False},
    {"uid": "E2003412B802011833303636", "nome": "Cartão do Ônibus", "obrigatorio": True},
]

# ── Rota GET /itens ───────────────────────────────────────────────────────────
@app.route("/itens", methods=["GET"])
def listar_itens():
    return jsonify({
        "itens": ITENS_MOCK,
        "total": len(ITENS_MOCK)
    }), 200

# ── Rota DELETE /itens/<uid> ──────────────────────────────────────────────────
@app.route("/itens/<uid>", methods=["DELETE"])
def remover_item(uid):
    for item in ITENS_MOCK:
        if item["uid"] == uid:
            ITENS_MOCK.remove(item)
            return jsonify({
                "mensagem": "Item removido com sucesso.",
                "uid": uid
            }), 200

    return jsonify({
        "erro": f"Item com UID '{uid}' não encontrado."
    }), 404

# ── Inicialização ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True)
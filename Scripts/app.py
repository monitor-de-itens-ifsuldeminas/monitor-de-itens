from flask import Flask, request, jsonify

app = Flask(__name__)

ITENS_MOCK = [
    {"uid": "E2003412B802011833303632", "nome": "Chave de Casa",  "obrigatorio": True},
    {"uid": "E2003412B802011833303633", "nome": "Carteira",       "obrigatorio": True},
    {"uid": "E2003412B802011833303634", "nome": "Crachá IFSUL",   "obrigatorio": True},
]

@app.route("/itens", methods=["POST"] )
def cadastrar_item():
    dados = request.get_json()

    if not dados or "uid" not in dados or "nome" not in dados or "obrigatorio" not in dados:
        return jsonify({"erro": "Campos 'uid', 'nome' e 'obrigatorio' são obrigatórios."}), 400
    
    uid = dados["uid"]
    nome = dados["nome"]
    obrigatorio = ["obrigatorio"]

    for item in ITENS_MOCK:
        if item["uid"]  == uid:
            return jsonify({"erro": "Já existe um item cadastrado com este UID."}), 409
        
        novo_item = {"uid": uid, "nome": nome, "obrigatorio": obrigatorio}
        ITENS_MOCK.append(novo_item)

        return jsonify({"mensagem": "Item cadastrado com sucesso.", "item": novo_item}), 201
    
    if __name__ == "__main__":
        app.run(debug=True)
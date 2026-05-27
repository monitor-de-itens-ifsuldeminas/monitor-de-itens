from flask import Flask, request, jsonify

app = Flask(__name__)

ultimo_uid_lido = "E2003412B802011833303699"


@app.route("/cadastrar-uid", methods=["POST"])
def cadastrar_uid():
    global ultimo_uid_lido
    dados = request.get_json()

    if not dados or "uid" not in dados:
        return jsonify({"erro": "O campo 'uid' é obrigatório."}), 400

    ultimo_uid_lido = dados["uid"]
    return jsonify({
        "mensagem": "UID recebido e armazenado com sucesso.",
        "uid": ultimo_uid_lido
    }), 200


@app.route("/ler-uid", methods=["GET"])
def ler_uid():
    if ultimo_uid_lido is None:
        return jsonify({"uid": None, "status": "aguardando"}), 200

    return jsonify({"uid": ultimo_uid_lido, "status": "disponivel"}), 200


if __name__ == "__main__":
    app.run(debug=True)
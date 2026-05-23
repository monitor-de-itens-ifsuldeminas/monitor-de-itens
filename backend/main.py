import sys
import io
from flask import Flask
from flask_cors import CORS

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

def create_app():
    app = Flask(__name__)

    app.config["JSON_AS_ASCII"] = False
    app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True

    CORS(app)

    # Registrar blueprints aqui quando as rotas chegarem

    @app.route("/health")
    def health():
        return {"status": "ok", "mensagem": "API no ar"}, 200

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
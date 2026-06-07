from app.routes.itens import itens_bp
from app.routes.uid_buffer import uid_buffer_bp
from app.routes.processar import processar_bp

def register_blueprints(app):
    app.register_blueprint(itens_bp)
    app.register_blueprint(uid_buffer_bp)
    app.register_blueprint(processar_bp)
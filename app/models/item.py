from app.database import db

class Item(db.Model):
    __tablename__ = "itens"

    id          = db.Column(db.Integer, primary_key=True)
    uid         = db.Column(db.String(50), nullable=False, unique=True)
    nome        = db.Column(db.String(100), nullable=False)
    obrigatorio = db.Column(db.Boolean, nullable=False, default=True)

    def to_dict(self):
        return {
            "uid":         self.uid,
            "nome":        self.nome,
            "obrigatorio": self.obrigatorio,
        }
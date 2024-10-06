from app import db


class Compras(db.Model):
    __tablename__ = "compras"
    id = db.Column(db.Integer, primary_key=True)
    producto_id = db.Column(db.Integer, db.ForeignKey("productos.id"))
    fecha_compra = db.Column(db.DateTime)
    direccion_envio = db.Column(db.String(255))
